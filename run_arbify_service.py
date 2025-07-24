import streamlit as st
from pages import Home, Game_History, Login, Register

def is_authenticated():
    return st.session_state.get("authenticated", False)

def home_page():
    Home.run()

def game_page():
    Game_History.run()

protected_pages = [
    st.Page(home_page, title="Arbify", icon="🏠"),
    st.Page(game_page, title="Game History", icon="🎲"),
]

# Auth or login/register page
def show_auth_gate():
    st.title("🔐 Please Log In or Register")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        Login.main()

    with tab2:
        Register.main()

# Routing logic
if is_authenticated():
    nav = st.navigation(protected_pages)
    nav.run()
else:
    show_auth_gate()