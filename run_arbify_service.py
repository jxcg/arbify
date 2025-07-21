import streamlit as st
from pages import Home, Game_History

def home_page():
    Home.run()

def game_page():
    Game_History.run()

pages = [
    st.Page(home_page, title="Arbify", icon="🏠"),
    st.Page(game_page, title="Game History", icon="🎲"),
]

pg = st.navigation(pages)
pg.run()