import sys
from typing import List, Tuple

import folium
import leafmap.foliumap as leafmap
import networkx as nx
import osmnx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from networkx.classes.multidigraph import MultiDiGraph
from streamlit_extras.app_logo import add_logo
from streamlit_extras.stateful_button import button
from streamlit_extras.switch_page_button import switch_page
from yaml.loader import SafeLoader

st.set_page_config(
    layout="wide",
    # initial_sidebar_state="expanded",
    page_title="Roadio",
    page_icon="🚗",
    menu_items={
        "Get Help": "https://www.github.com/nathanyaqueby/roadio/",
        "Report a bug": "https://www.github.com/nathanyaqueby/roadio/issues",
        "About": "https://www.github.com/nathanyaqueby/roadio/",
    },
)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

#roadio-your-all-encompassing-sustainable-route-planner > div > span
{
    text-align: center ;

}
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.egzxvld5 > div.block-container.css-z5fcl4.egzxvld4 > div:nth-child(1) > div > div:nth-child(6){
    display: none;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.header("Roadio: Your all-encompassing sustainable route planner")
st.markdown(
    """
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.egzxvld5 > div.block-container.css-z5fcl4.egzxvld4
    {
        max-width: 100%;
        padding : 10px 10px 0px 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

add_logo("media/logo small.png", height=100)

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)
with st.spinner(text="In progress..."):
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"],
    )

    name, authentication_status, username = authenticator.login("Login", "main")
    user_data = pd.read_csv("data/people-with-companies-clean.csv")

try:
    user_infomration = user_data.loc[
        (user_data["first_name"] == name.split(" ")[0])
        & (user_data["last_name"] == name.split(" ")[1])
    ]
except Exception as e:
    pass

shortest_paths = []
try:

    def get_location_from_address(address: str):
        try:
            locator = Nominatim(user_agent="roadio")
            location = locator.geocode(address)
        except GeocoderTimedOut:
            return get_location_from_address(address)

        return location.latitude, location.longitude

    st.cache()

    def get_graph(address_orig: str, address_dest: str):
        MARGIN = 0.1

        # find location by address
        location_orig = get_location_from_address(address_orig)
        location_dest = get_location_from_address(address_dest)

        north = max(location_orig[0], location_dest[0]) + MARGIN
        south = min(location_orig[0], location_dest[0]) - MARGIN
        west = max(location_orig[1], location_dest[1]) + MARGIN
        east = min(location_orig[1], location_dest[1]) - MARGIN

        print(f"North: {north}, South: {south}")
        print(f"West: {west}, East: {east}")

        graph = osmnx.graph.graph_from_bbox(
            north, south, east, west, network_type="drive", clean_periphery=False
        )

        return graph, location_orig, location_dest

    def get_graph_from_mode(
        address_orig: str,
        address_dest: str,
        mode: str,
        city: str = "Brussels",
        dist: float = 1000.0,
    ):
        assert mode in ["place", "address"]

        # find location by address
        location_orig = get_location_from_address(address_orig)
        location_dest = get_location_from_address(address_dest)

        if mode == "place":
            graph = osmnx.graph_from_place(city, network_type="drive")
        else:
            graph = osmnx.graph.graph_from_address(
                address_orig, dist=dist, dist_type="bbox", network_type="drive"
            )

        return graph, location_orig, location_dest

    def find_shortest_path(
        graph: MultiDiGraph,
        location_orig: Tuple[float],
        location_dest: Tuple[float],
        optimizer: str,
    ) -> List[int]:
        # find the nearest node to the departure and arrival location
        node_orig = osmnx.get_nearest_node(graph, location_orig)
        node_dest = osmnx.get_nearest_node(graph, location_dest)

        route = nx.shortest_path(graph, node_orig, node_dest, weight=optimizer.lower())
        return route, node_orig, node_dest

    def clear_text():
        st.session_state["go_from"] = ""
        st.session_state["go_to"] = ""

    ############ sidebar ############

    if st.session_state["authentication_status"]:
        with st.sidebar:
            st.title("Generate your route")
            basemap = "Satellite"

            col11, col12, col13 = st.columns([1, 1, 1])

            with col11:
                home_button = button("🏠 Home", key="home", use_container_width=True)
            with col12:
                work_button = button("🏢 Work", key="work", use_container_width=True)
            with col13:
                other_button = button("🔍 Other", key="other", use_container_width=True)

            if work_button:
                address_orig = user_infomration["address"].values[0]
                icon_orig = folium.Icon(color="green", icon="briefcase")
                address_dest = user_infomration["address_company"].values[0]
                icon_dest = folium.Icon(color="red", icon="home")
            elif other_button:
                icon_orig = folium.Icon(color="green", icon="info-sign")
                address_orig = st.text_input(
                    "Start address", "Am Kreuzhof 2, Regensburg"
                )
                icon_dest = folium.Icon(color="red", icon="info-sign")
                address_dest = st.text_input(
                    "Destination address", "Friedrich-Viehbacher-Allee 5, Regensburg"
                )
            else:
                address_orig = user_infomration["address_company"].values[0]
                icon_orig = folium.Icon(color="green", icon="home")
                address_dest = user_infomration["address"].values[0]
                icon_dest = folium.Icon(color="red", icon="briefcase")

            # st.subheader("Choose your mode of transport")
            mode = st.selectbox(
                "Mode of transport",
                ["🚗 Car", "🚲 Bike", "🛵 Motorcycle", "🛴 E-Scooter", "Other"],
            )
            if mode == "🚗 Car":
                value = 0.2
            elif mode == "🚲 Bike":
                value = 100
            elif mode == "🛵 Motorcycle":
                value = 0.3
            elif mode == "🛴 E-Scooter":
                value = 0.4
            else:
                value = 0.5

            # add CO2 emissions and heart rate as two columns
            col1, col2 = st.columns(2)
            with col1:
                st.image("media/roadio icons - 1.png")
                st.metric(label="CO2 Emissions", value="0.5 kg")
            with col2:
                st.image("media/roadio icons -2.png")
                st.metric(label="Health Benefits", value=f"{value} %")

            optimizer = "Travel time"

            # add two buttons: "Generate route" and "Go to carpooling"
            submit_button = st.button(
                "Generate route", type="primary", use_container_width=True
            )
            carpool_button = st.button(
                "Go to carpooling", type="secondary", use_container_width=True
            )

            st.markdown(
                f"<p style='text-align: center; color: black;'>UserName:  {st.session_state['name']}</p>",
                unsafe_allow_html=True,
            )
            authenticator.logout("Logout", "main", key="unique_key")
            st.markdown(
                """
            <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.css-vk3wp9.e1fqkh3o11 > div.css-6qob1r.e1fqkh3o3 > div.css-e3xfei.e1fqkh3o4 > div > div:nth-child(1) > div > div:nth-child(8) > div > button                {
                display:inline-block;   
                position: absolute;
                left:40%;
                right:40%;
                white-space: nowrap;
                margin:0px auto;
                text-align: center;
                }
            </style>
    """,
                unsafe_allow_html=True,
            )

        ############ main

        if optimizer == "Travel time":
            optimizer = "Time"

        lat, lon = get_location_from_address(address=address_orig)

        m = leafmap.Map(center=(lat, lon), zoom=16)

        m.add_basemap(basemap)

        if submit_button and address_orig and address_dest:
            # Find the route
            graph, location_orig, location_dest = get_graph(address_orig, address_dest)

            # re-center
            leafmap.Map(center=location_orig, zoom=16)

            # find the nearest node to the start location
            m.add_marker(
                location=list(location_orig),
                icon=folium.Icon(color="red", icon="suitcase", prefix="fa"),
                popup=f"{address_orig}",
            )
            m.add_marker(
                location=list(location_dest),
                icon=folium.Icon(color="green", icon="street-view", prefix="fa"),
                popup=f"{address_dest}",
            )

            # find the shortest path
            route, node_orig, node_dest = find_shortest_path(
                graph, location_orig, location_dest, optimizer
            )

            st.write(f"Nearest node to departure: {node_orig}")
            st.write(f"Nearest node to arrival: {node_dest}")

            # Append the shortest path to the list
            shortest_paths.append(
                {"Mode": mode, "Optimizer": optimizer, "Shortest Path": route}
            )

            osmnx.plot_route_folium(graph, route, m)

        if carpool_button:
            switch_page("Carpooling")

        else:
            m.add_marker(
                location=(lat, lon),
                popup=user_infomration["address"].values[0],
                icon=folium.Icon(color="green", icon="eye", prefix="fa"),
            )
            # st.write(f"Lat, Lon: {lat}, {lon}")

        m.to_streamlit(scrolling=True)

        # Display the dataframe of shortest paths
        if shortest_paths:
            df_shortest_paths = pd.DataFrame(shortest_paths)
            st.subheader("Shortest Paths")
            st.dataframe(df_shortest_paths)

    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")

except Exception as e:
    # st.error(e)
    st.write("UserName or Password not found")
