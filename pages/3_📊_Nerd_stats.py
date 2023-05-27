import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.app_logo import add_logo

st.set_page_config(
    layout="wide",
    # initial_sidebar_state="expanded",
    page_title="Nerd stats",
    page_icon="🚗",
    menu_items={
        "Get Help": "https://www.github.com/nathanyaqueby/roadio/",
        "Report a bug": "https://www.github.com/nathanyaqueby/roadio/issues",
        "About": "https://www.github.com/nathanyaqueby/roadio/",
    },
)

add_logo("media/logo small.png", height=100)

st.title("Nerd stats")
st.markdown(
    "Did you get tired of all the fancy pictures? Here are some numbers for you!"
)

st.sidebar.image("media/turm transparent.png", use_column_width=True)

# plot CO2 emissions
# st.subheader("CO2 emissions")

# load data roadio/data/owid-co2-data.csv
df = pd.read_csv("data/owid-co2-data.csv")

# plot the co2 emissions and highlight germany
fig = px.line(df, x="year", y="cumulative_co2", color="country")
fig.update_layout(
    title="CO2 emissions per country",
    xaxis_title="Year",
    yaxis_title="CO2 emissions (kt)",
    legend_title="Country",
    font=dict(family="Courier New, monospace", size=18, color="RebeccaPurple"),
)
st.plotly_chart(fig, use_container_width=True)
