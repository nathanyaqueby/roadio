import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

############ sidebar

st.sidebar.header("Insert your home address")
address = st.sidebar.text_input("Address", "Am Kreuzhof 2, Regensburg")

# get location from address
lat, lon = get_location_from_address(address)

st.sidebar.header("Insert your work address")
work_address = st.sidebar.text_input("Address", "Friedrich-Viehbacher-Allee 5, Regensburg")

# get location from address
work_lat, work_lon = get_location_from_address(work_address)

############ main

mapbox_access_token = st.secrets["mapbox_access_token"]

people_data = pd.read_csv('people-with-addresses.csv')
people_data['full_name'] = people_data[['first_name','last_name']].apply(lambda x: ' '.join(x), axis=1)

company_data = pd.read_csv('ratisbona-companies.csv')

fig = go.Figure()

# People
fig.add_trace(go.Scattermapbox(
        lat=people_data.lat,
        lon=people_data.lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color='rgb(255, 60, 60)',
            opacity=0.7
        ),
        text=people_data.full_name,
        name="People"
    ))

# Companies
fig.add_trace(go.Scattermapbox(
        lat=company_data.lat,
        lon=company_data.lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color='rgb(60, 60, 255)',
            opacity=0.7
        ),
        text=company_data.name,
        name="Companies"
    ))

fig.update_layout(
    hovermode='closest',
    width=1024,
    height=768,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=49.0134,
            lon=12.1016
        ),
        pitch=0,
        zoom=9
    )
)

# add route
fig.add_trace(go.Scattermapbox(
        lat=[lat, work_lat],
        lon=[lon, work_lon],
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=10,
            color='rgb(60, 255, 60)',
            opacity=0.7
        ),
        text="Route",
        name="Route"
    ))

st.plotly_chart(fig, use_container_width=True)