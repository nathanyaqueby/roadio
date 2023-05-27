import sys
from typing import List, Tuple

import folium
import leafmap.foliumap as leafmap
import networkx as nx
import osmnx
import osmnx as ox
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
    page_title="Carpooling",
    page_icon="🚗",
    menu_items={
        "Get Help": "https://www.github.com/nathanyaqueby/roadio/",
        "Report a bug": "https://www.github.com/nathanyaqueby/roadio/issues",
        "About": "https://www.github.com/nathanyaqueby/roadio/",
    },
)

add_logo("media/logo small.png", height=100)

st.title("Carpooling")

###################### sidebar ######################
with st.sidebar:
    st.title("Offer a ride")

    # dropdown to select car type
    car_type = st.selectbox("Car type", ["Minivan", "Sedan", "SUV", "Truck", "Van"])

    # set up the max number of seats based on car type
    if car_type == "Minivan":
        max_seats = 7
    elif car_type == "Sedan":
        max_seats = 5
    elif car_type == "SUV":
        max_seats = 8
    elif car_type == "Truck":
        max_seats = 3
    elif car_type == "Van":
        max_seats = 9

    # slider to select number of open seats
    open_seats = st.slider("Number of open seats", 0, max_seats, 3)

    # button to find matches
    find_matches = st.button("Find matches", type="primary", use_container_width=True)

    # add image at the bottom
    st.image("media/turm transparent.png", use_column_width=True)


with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)
name, authentication_status, username = authenticator.login("Login", "main")
user_data = pd.read_csv("data/people-with-companies-clean.csv")


###################### helper ######################
def get_location_from_address(address: str):
    try:
        locator = Nominatim(user_agent="roadio")
        location = locator.geocode(address)
    except GeocoderTimedOut:
        return get_location_from_address(address)

    return location.latitude, location.longitude


###################### main ######################

try:
    user_infomration = user_data.loc[
        (user_data["first_name"] == name.split(" ")[0])
        & (user_data["last_name"] == name.split(" ")[1])
    ]
except Exception as e:
    pass


def get_distance(origin, destination):
    return ox.distance.great_circle_vec(*origin, *destination)


center_origin = user_infomration["lat"].values[0], user_infomration["lon"].values[0]
center_origin_company = (
    user_infomration["lat_company"].values[0],
    user_infomration["lon_company"].values[0],
)
driver_distaance = get_distance(center_origin, center_origin_company)
# st.write(driver_distaance)

for data in user_data.iterrows():
    user_data["distance_from_driver"] = get_distance(
        center_origin, (user_data["lat"], user_data["lon"])
    )
    user_data["distance_from_dest"] = get_distance(
        (user_data["lat"], user_data["lon"]),
        (user_data["lat_company"], user_data["lon_company"]),
    )
    user_data["distance_dest"] = get_distance(
        center_origin_company, (user_data["lat_company"], user_data["lon_company"])
    )
user_data = user_data[user_data["distance_from_driver"] > driver_distaance]


# filter out the driver
car_pool_user = user_data.sort_values(
    ["distance_from_driver", "distance_dest"], ascending=[False, False]
).iloc[1 : open_seats + 1, :]

# print all the matches
st.write(car_pool_user)

m = leafmap.Map(
    center=(user_infomration["lat"].values[0], user_infomration["lon"].values[0]),
    zoom=12,
)
m.add_basemap("Satellite")

# add marker for the origin
m.add_marker(
    location=(user_infomration["lat"].values[0], user_infomration["lon"].values[0]),
    popup="Origin",
    icon=folium.Icon(color="green", icon="home"),
)

# add marker for the destination
m.add_marker(
    location=(
        user_infomration["lat_company"].values[0],
        user_infomration["lon_company"].values[0],
    ),
    popup="Destination",
    icon=folium.Icon(color="red", icon="flag"),
)

# add markers for each latitute and longitude in car_pool_user
for data in car_pool_user.iterrows():
    m.add_marker(
        location=(data[1]["lat"], data[1]["lon"]),
        popup=data[1]["first_name"]
        + " "
        + data[1]["last_name"]
        + " "
        + data[1]["address_company"],
    )

m.to_streamlit(scrolling=True)
