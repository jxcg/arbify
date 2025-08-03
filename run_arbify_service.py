import streamlit as st
from pages import Home, Game_History, Login, Register
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(password=st.secrets["cookie_password"])
if not cookies.ready():
    st.stop()


def is_authenticated():
    return cookies.get("user_id") is not None




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
        Login.login_page(cookies)

    with tab2:
        Register.main()

# Routing logic
if is_authenticated():
    nav = st.navigation(protected_pages)
    if st.button("Logout"):
        cookies["user_id"] = ""
        cookies["username"] = ""
    nav.run()
else:
    show_auth_gate()