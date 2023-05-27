import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_card import card
# from awesome_table import AwesomeTable
# from awesome_table.columns import (Column, ColumnDType)
from streamlit_extras.app_logo import add_logo

# from streamlit_extras.dataframe_explorer import dataframe_explorer

st.set_page_config(
    layout="wide",
    # initial_sidebar_state="expanded",
    page_title="Leaderboard",
    page_icon="🚗",
    menu_items={
        "Get Help": "https://www.github.com/nathanyaqueby/roadio/",
        "Report a bug": "https://www.github.com/nathanyaqueby/roadio/issues",
        "About": "https://www.github.com/nathanyaqueby/roadio/",
    },
)

add_logo("media/logo small.png", height=100)

st.sidebar.image("media/turm transparent.png", use_column_width=True)

st.title("Leaderboard")
st.markdown(
    "See how much sustainable travel you've done and how you compare to others!"
)

col21, col22, col23, col24 = st.columns([1, 1, 1, 1])
with col21:
    st.image("https://imgtr.ee/images/2023/05/26/we9tL.png")

with col22:
    st.image("https://imgtr.ee/images/2023/05/26/wenbF.png")

with col23:
    st.image("https://imgtr.ee/images/2023/05/26/weyhm.png")

with col24:
    st.image("https://imgtr.ee/images/2023/05/26/we0XU.png")

sample_data = {
    "Rank 🏆": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Name ✏️": [
        "Liesa McMinn",
        "Nathan Yaqueby",
        "John Doe",
        "Jane Doe",
        "John Smith",
        "Jane Smith",
        "John Doe",
        "Jane Doe",
        "John Smith",
        "Jane Smith",
    ],
    "Company 🏢": [
        "Vitesco",
        "McDonald's",
        "Vitesco",
        "McDonald's",
        "Vitesco",
        "McDonald's",
        "Vitesco",
        "McDonald's",
        "Vitesco",
        "McDonald's",
    ],
    "XP ⬆️": [1000, 900, 800, 700, 600, 500, 400, 300, 200, 100],
    "Gems 💎": [1200, 1100, 1000, 900, 800, 700, 600, 500, 400, 300],
    "CO2 Saved (kg) ⛽": [100, 90, 80, 70, 60, 50, 40, 30, 20, 10],
    "Travelled (km) 🛞": [1000, 900, 800, 700, 600, 500, 400, 300, 200, 100],
    "Journey Count 🧳": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    "Transportation mode 🚗": [
        "Car",
        "Motorcycle",
        "Bike",
        "Car",
        "Motorcycle",
        "Bike",
        "Car",
        "Motorcycle",
        "Bike",
        "Car",
    ],
}

# filtered_df = dataframe_explorer(sample_data, case=False)
st.dataframe(sample_data, use_container_width=True)

# AwesomeTable(pd.read_json(sample_data), columns=[
#     Column(name='id', label='ID'),
#     Column(name='name', label='Name'),
#     Column(name='job_title', label='Job Title'),
#     Column(name='avatar', label='Avatar', dtype=ColumnDType.IMAGE),
#     Column(name='_url.social_media', label='Social Media', dtype=ColumnDType.ICONBUTTON, icon='fa-solid fa-share-nodes'), ## From FontAwesome v6.0.0
#     Column(name='_url.document', label='Document', dtype=ColumnDType.DOWNLOAD),
# ], show_search=True, show_order=True)
