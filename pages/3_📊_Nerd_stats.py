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
    "Did you get tired of all the fancy pictures? Here are some numbers to feed your inner nerd."
)
with st.spinner("Loading Stats..."):
    st.sidebar.image("media/turm transparent.png", use_column_width=True)
    # plot CO2 emissions
    # st.subheader("CO2 emissions")

    # load data roadio/data/owid-co2-data.csv
    df = pd.read_csv("data/owid-co2-data.csv")

    # split into two columns
    col31, col32 = st.columns(2, gap="small")

    with col31:
        # st.subheader("Global GHG emissions")
        # plot the ghg emissions for the top 10 countries with the highest emissions and germany
        ctry_list = [
            "Germany",
            "United States",
            "China",
            "India",
            "Russia",
            "Japan",
            "Brazil",
            "United Kingdom",
            "Iran",
            "Canada",
            "Italy",
        ]
        df_c = df[df["country"].isin(ctry_list)]
        df_c = df_c[df_c["year"] >= 1800]
        fig = px.line(df_c, x="year", y="cumulative_co2", color="country")
        fig.update_layout(
            title="CO2 emissions per country",
            xaxis_title="Year",
            yaxis_title="CO2 emissions (kt)",
            legend_title="Country",
            font=dict(family="Courier New, monospace", size=18, color="RebeccaPurple"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col32:
        # get data from df_c with year 1965 onwards
        df_c = df_c[df_c["year"] >= 1965]
        # plot the energy consumption per capita for df_c as a pie chart
        fig = px.pie(
            df_c,
            values="cumulative_co2",
            names="country",
            title="CO2 emissions per country",
        )
        st.plotly_chart(fig, use_container_width=True)

    # plot the co2 emissions as a 3d scatter plot
    fig = px.scatter_3d(
        df_c, x="year", y="cumulative_co2", z="consumption_co2", color="country"
    )
    st.plotly_chart(fig, use_container_width=True)
