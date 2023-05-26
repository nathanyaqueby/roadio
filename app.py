import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import folium
import osmnx
import networkx as nx
import leafmap.foliumap as leafmap
from typing import Tuple, List
from networkx.classes.multidigraph import MultiDiGraph

import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def login():
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username == "admin" and password == "password":
            st.success("Logged in successfully!")
            # Continue with the application logic after successful login
        else:
            st.error("Invalid username or password")

st.set_page_config(layout="wide",
                initial_sidebar_state="expanded",
                page_title="Roadio",
                page_icon="🚗",
                menu_items={
                    'Get Help': 'https://www.github.com/nathanyaqueby/roadio/',
                    'Report a bug': "https://www.github.com/nathanyaqueby/roadio/issues",
                    'About': "https://www.github.com/nathanyaqueby/roadio/"
                })

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

shortest_paths = []

############
@st.cache
def get_location_from_address(address: str):
    from geopy.geocoders import Nominatim

    locator = Nominatim(user_agent = "roadio")
    location = locator.geocode(address)

    return location.latitude, location.longitude

@st.cache
def get_graph(address_orig: str, address_dest: str):

    MARGIN = 0.1

    # find location by address
    location_orig = get_location_from_address(address_orig)
    location_dest = get_location_from_address(address_dest)

    north = max(location_orig[0],location_dest[0]) + MARGIN
    south = min(location_orig[0],location_dest[0]) - MARGIN
    west = max(location_orig[1],location_dest[1]) + MARGIN
    east = min(location_orig[1],location_dest[1]) - MARGIN

    print(f'North: {north}, South: {south}')
    print(f'West: {west}, East: {east}')

    graph = osmnx.graph.graph_from_bbox(north, south, east, west, network_type='drive', clean_periphery=False)

    return graph, location_orig, location_dest

@st.cache
def get_graph_from_mode(address_orig: str, address_dest: str, mode: str, city: str="Brussels", dist: float=1000.):

    assert mode in ['place', 'address']

    # find location by address
    location_orig = get_location_from_address(address_orig)
    location_dest = get_location_from_address(address_dest)

    if mode == 'place':
        graph = osmnx.graph_from_place(city, network_type = 'drive')
    else:
        graph = osmnx.graph.graph_from_address(address_orig, dist=dist, dist_type='bbox', network_type = 'drive')

    return graph, location_orig, location_dest

@st.cache
def find_shortest_path(graph: MultiDiGraph, location_orig: Tuple[float], location_dest: Tuple[float], optimizer: str) -> List[int]:
    # find the nearest node to the departure and arrival location
    node_orig = osmnx.get_nearest_node(graph, location_orig)
    node_dest = osmnx.get_nearest_node(graph, location_dest)

    st.write(f'Nearest node to departure: {node_orig}')
    st.write(f'Nearest node to arrival: {node_dest}')
    
    route = nx.shortest_path(graph, node_orig, node_dest, weight=optimizer.lower())
    return route

def clear_text():
    st.session_state["go_from"] = ""
    st.session_state["go_to"] = ""

############ sidebar

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{st.session_state["name"]}*!')
    
    with st.sidebar:

        with st.form(key='generate_route'):
            st.title("Generate your route")

            basemap = st.selectbox("Choose basemap", ['Satellite', 'Roadmap', 'Terrain', 'Hybrid', 'OpenStreetMap'])
            if basemap in ['Satellite', 'Roadmap', 'Terrain', 'Hybrid', 'OpenStreetMap'][:-1]:
                basemap=basemap.upper()

            # st.subheader("Choose your mode of transport")
            mode = st.selectbox("Mode of transport", ["🚗 Car", "🚲 Bike", "🛵 Motorcycle", "🛴 E-Scooter", "Other"])
            
            # st.subheader("Choose your optimizer")
            optimizer = st.selectbox("Route optimizer", ["Distance ", "Travel time"])

            # st.subheader("Choose your departure location")
            # give radio choices between home, work, or other
            address_options = ["🏠 Home", "🏢 Work", "Other"]
            address_orig = st.radio("Departure location", address_options, index=0)
            if address_orig == "Home":
                address_orig = "Am Kreuzhof 2, Regensburg"
                icon_orig = folium.Icon(color="green", icon="home")
                # write the address in the sidebar
                st.write(address_orig)
            elif address_orig == "Work":
                address_orig = "Friedrich-Viehbacher-Allee 5, Regensburg"
                icon_orig = folium.Icon(color="green", icon="briefcase")
                # write the address in the sidebar
                st.write(address_orig)
            else:
                icon_orig = folium.Icon(color="green", icon="info-sign")
                # user input
                address_orig = st.text_input("Address", "Am Kreuzhof 2, Regensburg")
            
            # do the same for the destination
            # TO-DO: if the user selected "home" for the departure, then the destination is "work" and vice versa
            # st.subheader("Choose your destination")
            address_dest = st.radio("Destination", address_options, index=1)
            if address_dest == "Home":
                address_dest = "Am Kreuzhof 2, Regensburg"
                icon_dest = folium.Icon(color="red", icon="home")
                # write the address in the sidebar
                st.write(address_dest)
            elif address_dest == "Work":
                address_dest = "Friedrich-Viehbacher-Allee 5, Regensburg"
                icon_dest = folium.Icon(color="red", icon="briefcase")
                # write the address in the sidebar
                st.write(address_dest)
            else:
                icon_dest = folium.Icon(color="red", icon="info-sign")
                # user input
                address_dest = st.text_input("Address", "Friedrich-Viehbacher-Allee 5, Regensburg")

            # submit button
            submit_button = st.form_submit_button(label='Generate route',
                                                help='Click to generate your route',
                                                type='primary',
                                                use_container_width=True)

    ############ main

    st.title("Roadio: Your all-encompassing sustainable route planner")

    if optimizer == "Distance":
        optimizer = "Length"
    elif optimizer == "Travel time":
        optimizer = "Time"

    lat, lon = get_location_from_address(address=address_orig)

    m = leafmap.Map(center=(lat, lon), zoom=16)

    m.add_basemap(basemap)

    if submit_button and address_orig and address_dest:

        # Find the route
        graph, location_orig, location_dest = get_graph(address_orig, address_dest)

        # Search information 
        # st.markdown(f'**From**: {address_orig}')
        # st.markdown(f'**To**: {address_dest}')
        # st.write(graph)

        # re-center
        leafmap.Map(center=location_orig, zoom=16)

        # find the nearest node to the start location
        m.add_marker(location=list(location_orig), icon=folium.Icon(color='red', icon='suitcase', prefix='fa'), popup=f"{address_orig}")
        m.add_marker(location=list(location_dest), icon=folium.Icon(color='green', icon='street-view', prefix='fa'), popup=f"{address_dest}")

        # find the shortest path
        route = find_shortest_path(graph, location_orig, location_dest, optimizer)

        # Append the shortest path to the list
        shortest_paths.append({
            'Mode': mode,
            'Optimizer': optimizer,
            'Shortest Path': route
        })

        osmnx.plot_route_folium(graph, route, m)

    else:

        m.add_marker(location=(lat, lon), popup=f"lat, lon: {lat}, {lon}", icon=folium.Icon(color='green', icon='eye', prefix='fa'))
        # st.write(f"Lat, Lon: {lat}, {lon}")


    m.to_streamlit(scrolling=True)

    # Display the dataframe of shortest paths
    if shortest_paths:
        df_shortest_paths = pd.DataFrame(shortest_paths)
        st.subheader("Shortest Paths")
        st.dataframe(df_shortest_paths)

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

# mapbox_access_token = st.secrets["mapbox_access_token"]

# people_data = pd.read_csv('people-with-addresses.csv')
# people_data['full_name'] = people_data[['first_name','last_name']].apply(lambda x: ' '.join(x), axis=1)

# company_data = pd.read_csv('ratisbona-companies.csv')

# fig = go.Figure()

# # People
# fig.add_trace(go.Scattermapbox(
#         lat=people_data.lat,
#         lon=people_data.lon,
#         mode='markers',
#         marker=go.scattermapbox.Marker(
#             size=10,
#             color='rgb(255, 60, 60)',
#             opacity=0.7
#         ),
#         text=people_data.full_name,
#         name="People"
#     ))

# # Companies
# fig.add_trace(go.Scattermapbox(
#         lat=company_data.lat,
#         lon=company_data.lon,
#         mode='markers',
#         marker=go.scattermapbox.Marker(
#             size=10,
#             color='rgb(60, 60, 255)',
#             opacity=0.7
#         ),
#         text=company_data.name,
#         name="Companies"
#     ))

# fig.update_layout(
#     hovermode='closest',
#     width=1024,
#     height=768,
#     mapbox=dict(
#         accesstoken=mapbox_access_token,
#         bearing=0,
#         center=go.layout.mapbox.Center(
#             lat=49.0134,
#             lon=12.1016
#         ),
#         pitch=0,
#         zoom=9
#     )
# )

# # add route
# fig.add_trace(go.Scattermapbox(
#         lat=[lat, work_lat],
#         lon=[lon, work_lon],
#         mode='lines',
#         marker=go.scattermapbox.Marker(
#             size=10,
#             color='rgb(60, 255, 60)',
#             opacity=0.7
#         ),
#         text="Route",
#         name="Route"
#     ))

# st.plotly_chart(fig, use_container_width=True)