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

st.set_page_config(layout="wide",
                initial_sidebar_state="expanded",
                page_title="Roadio",
                page_icon="🚗"
                )

############
def get_location_from_address(address: str):
    from geopy.geocoders import Nominatim

    locator = Nominatim(user_agent = "roadio")
    location = locator.geocode(address)

    return location.latitude, location.longitude

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

def find_shortest_path(graph: MultiDiGraph, location_orig: Tuple[float], location_dest: Tuple[float], optimizer: str) -> List[int]:
    # find the nearest node to the departure and arrival location
    node_orig = osmnx.get_nearest_node(graph, location_orig)
    node_dest = osmnx.get_nearest_node(graph, location_dest)

    route = nx.shortest_path(graph, node_orig, node_dest, weight=optimizer.lower())
    return route

def clear_text():
    st.session_state["go_from"] = ""
    st.session_state["go_to"] = ""
############ sidebar

with st.sidebar:

    with st.form(key='generate_route'):
        st.header("Generate your route")

        basemap = st.selectbox("Choose basemap", ['Satellite', 'Roadmap', 'Terrain', 'Hybrid', 'OpenStreetMap'])
        if basemap in ['Satellite', 'Roadmap', 'Terrain', 'Hybrid', 'OpenStreetMap'][:-1]:
            basemap=basemap.upper()

        st.subheader("Choose your mode of transport")
        mode = st.selectbox("Mode", ["Car", "Bike", "Motorcycle", "E-Scooter", "Other"])
        
        st.subheader("Choose your optimizer")
        optimizer = st.selectbox("Optimizer", ["Distance", "Travel time"])

        st.subheader("Choose your departure location")
        address_orig = st.text_input("Address", "Am Kreuzhof 2, Regensburg")
        
        st.subheader("Choose your destination location")
        address_dest = st.text_input("Address", "Friedrich-Viehbacher-Allee 5, Regensburg")
        submit_button = st.form_submit_button(label='Generate route')

############ main

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
    st.markdown(f'**From**: {address_orig}')
    st.markdown(f'**To**: {address_dest}')
    st.write(graph)

    # re-center
    leafmap.Map(center=location_orig, zoom=16)

    # find the nearest node to the start location
    m.add_marker(location=list(location_orig), icon=folium.Icon(color='red', icon='suitcase', prefix='fa'))
    m.add_marker(location=list(location_dest), icon=folium.Icon(color='green', icon='street-view', prefix='fa'))

    # find the shortest path
    route = find_shortest_path(graph, location_orig, location_dest, optimizer)

    osmnx.plot_route_folium(graph, route, m)

else:

    m.add_marker(location=(lat, lon), popup=f"lat, lon: {lat}, {lon}", icon=folium.Icon(color='green', icon='eye', prefix='fa'))
    st.write(f"Lat, Lon: {lat}, {lon}")


m.to_streamlit(scrolling=True)

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