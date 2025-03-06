import streamlit as st
import requests

st.set_page_config(page_title="Login - SIGMA Learning", page_icon="🔑")

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
            .nav-links {
            font-size: 16px;
            color: #00D9FF;
            text-decoration: none;
            cursor: pointer;
            text-align: center;
            margin-top: 10px;
            display: block;
        }
        .nav-links:hover {
            text-decoration: underline;
        }
            
        .admin-button {
            background: linear-gradient(45deg, #00D9FF, #0070FF);
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 12px 25px;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            text-align: center;
            margin-top: 15px;
            display: block;
            width: 220px;
            text-transform: uppercase;
            transition: all 0.3s ease;
        }
        .admin-button:hover {
            background: linear-gradient(45deg, #0070FF, #00D9FF);
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000/auth"

st.title("SIGMA Learning Platform")
st.subheader("Login")

# Login Form
login_username = st.text_input("Username", key="login_username")
login_password = st.text_input("Password", type="password", key="login_password")

if st.button("Login"):
    try:
        response = requests.post(f"{BACKEND_URL}/login", json={
            "username": login_username,
            "password": login_password
        })
        if response.status_code == 200:
            st.success("Login successful!")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")

# Navigate to Register Page (Fixed Navigation)
col1, col2, col3 = st.columns([1, 3, 1])  # Center the text link
with col2:
    if st.button("Don't have an account? Register here", key="go_to_register", help="Click to navigate to the register page"):
        st.switch_page("pages/register.py")
    
    if st.button("Forgot your password? Reset it here", key="go_to_reset_password", help="Click to navigate to reset password page"):
        st.switch_page("pages/reset_password.py")
    
    # Admin Login Navigation Button
    if st.button("Admin Login", key="go_to_admin", help="Click to navigate to the admin login page"):
        st.switch_page("pages/adminlogin.py")
