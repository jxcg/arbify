import streamlit as st
from pages import Home, Game_History
import streamlit_cookies_manager


def home_page():
    Home.run()



def game_page():
    Game_History.run()


protected_pages = [
    st.Page(home_page, title="Arbify", icon="🏠"),
    st.Page(game_page, title="Game History", icon="🎲"),
]
st.set_page_config(layout="wide")
nav = st.navigation(protected_pages)
nav.run()