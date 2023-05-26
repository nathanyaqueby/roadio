import streamlit as st

st.set_page_config(layout="wide",
                initial_sidebar_state="expanded",
                page_title="Roadio",
                page_icon="🚗",
                menu_items={
                    'Get Help': 'https://www.github.com/nathanyaqueby/roadio/',
                    'Report a bug': "https://www.github.com/nathanyaqueby/roadio/issues",
                    'About': "https://www.github.com/nathanyaqueby/roadio/"
                })

st.title("Leaderboard")