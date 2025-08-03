import streamlit as st
from auth.auth_manager import login_user

def login_page(cookies):
    st.title("🔐 Login")

    usn = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if not usn or not pw:
            st.warning("Please fill out both fields.")
        else:
            user_id = login_user(usn, pw)
            if user_id:
                # Set session state
                st.session_state['user_id'] = str(user_id)
                st.session_state['username'] = usn
                
                # Set cookies
                cookies['user_id'] = str(user_id)
                cookies['username'] = usn
                if hasattr(cookies, 'save'):
                    cookies.save()
                
                st.rerun()
            else:
                st.error("Invalid username or password.")
