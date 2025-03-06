import streamlit as st
import requests

st.set_page_config(page_title="Register - SIGMA Learning", page_icon="📝")

# Custom CSS
st.markdown("""
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #121212;
            color: #f0f0f0;
            padding: 0;
            margin: 0;
            overflow: hidden;
            height: 100vh;
        }
        .stTextInput>div>input {
            background-color: #333333;
            color: white;
            border: 2px solid #0070FF;
            padding: 10px;
            border-radius: 8px;
            font-size: 18px;
        }
        .stButton>button {
            background-color: #0070FF;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #00D9FF;
        }
        .login-link {
            font-size: 16px;
            color: #00D9FF;
            text-decoration: none;
            cursor: pointer;
            display: block;
            text-align: center;
            margin-top: 10px;
        }
        .login-link:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000/auth"

st.title("SIGMA Learning Platform")
st.subheader("Register")

# Registration Form
reg_username = st.text_input("Username", key="reg_username")
reg_email = st.text_input("Email", key="reg_email")
reg_password = st.text_input("Password", type="password", key="reg_password")

if st.button("Register"):
    try:
        response = requests.post(f"{BACKEND_URL}/register", json={
            "username": reg_username,
            "email": reg_email,
            "password": reg_password
        })
        if response.status_code == 201:
            st.success(response.json().get("message", "Registration successful"))
            st.session_state.user_logged_in = True
            st.switch_page("pages/learners_dashboard.py")

        else:
            st.error(response.json().get("error", "Registration failed"))
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")

# Navigate to Login Page (Fixed Navigation)
col1, col2, col3 = st.columns([1, 3, 1])  # Center the text link
with col2:
    if st.button("Already have an account? Click here to login", key="go_to_login", help="Click to navigate to the login page"):
        st.switch_page("pages/login.py")
