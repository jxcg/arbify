import streamlit as st
from auth.register_user import create_user, username_exists

def main():
    st.title("📝 Register New Account")

    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email (optional)")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register")

        if submitted:
            if not username or not password:
                st.error("Username and password are required.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif username_exists(username):
                st.warning("That username is already taken.")
            else:
                success = create_user(username, password, email)
                if success:
                    st.success("✅ Account created! You can now log in.")
                else:
                    st.error("❌ Something went wrong. Try again.")

if __name__ == "__main__":
    main()
