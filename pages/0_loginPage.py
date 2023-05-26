import streamlit as st
from streamlit.hashing import _CodeHasher
from getpass import getpass

def login():
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if authenticate_user(username, password):
            session_state = create_session_state(username)
            st.success("Logged in successfully!")
            app(session_state)
        else:
            st.error("Invalid username or password")

def authenticate_user(username, password):
    # Replace this with your own authentication logic
    if username == "admin" and password == "password":
        return True
    else:
        return False

def create_session_state(username):
    # Generate a unique hash for the session
    session_id = _CodeHasher().to_bytes(username, 32)[:16].hex()
    return {"username": username, "session_id": session_id}

def app(session_state):
    st.title("Authenticated App")
    st.write(f"Welcome, {session_state['username']}!")
    # Add your application logic here

def main():
    session_state = st.session_state.get("session_state", None)
    if session_state is None:
        login()
    else:
        app(session_state)

if __name__ == "__main__":
    main()
