import streamlit as st
from pages import Home, Calculator, Game_History

def home_page():
    Home.run()

def calculator_page():
    Calculator.run()

def game_page():
    Game_History.run()

pages = [
    st.Page(home_page, title="Arbify", icon="🏠"),
    st.Page(calculator_page, title="Bet Calculator", icon="🧮"),
    st.Page(game_page, title="Game History", icon="🎲"),
]

pg = st.navigation(pages)
pg.run()