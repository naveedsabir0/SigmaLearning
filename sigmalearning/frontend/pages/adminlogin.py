import streamlit as st
import requests

st.set_page_config(page_title="Admin Login - SIGMA Learning", page_icon="🛠️")

# Custom CSS for Futuristic Design
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;700&family=Exo:wght@400;700&display=swap');
        body {
            font-family: 'Orbitron', sans-serif;
            background-color: #0a0a0a;
            color: white;
            text-align: center;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            max-width: 500px;
            margin: auto;
            position: relative;
            z-index: 1;
            background: rgba(255, 255, 255, 0.05);
            padding: 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0px 0px 15px rgba(0, 255, 255, 0.3);
        }
        .title {
            font-size: 36px;
            font-weight: 700;
            color: #00FFFF;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .subtitle {
            font-size: 18px;
            font-weight: 300;
            color: #EAEAEA;
            margin-bottom: 30px;
        }
        .stTextInput>div>input {
            background-color: #222222;
            color: white;
            border: 2px solid #00D9FF;
            padding: 12px;
            border-radius: 10px;
            font-size: 18px;
        }
        .stButton>button {
            background: linear-gradient(45deg, #00D9FF, #0070FF);
            color: white;
            font-size: 18px;
            padding: 12px 20px;
            border-radius: 30px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
        }
        .stButton>button:hover {
            background: linear-gradient(45deg, #0070FF, #00D9FF);
            transform: scale(1.05);
        }
        .back-link {
            font-size: 16px;
            color: #00D9FF;
            text-decoration: none;
            cursor: pointer;
            display: block;
            margin-top: 20px;
        }
        .back-link:hover {
            text-decoration: underline;
        }
        .video-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }
        .video-background video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.3;
        }
    </style>
    <div class="video-background">
        <video autoplay loop muted playsinline>
            <source src="https://cdn.pixabay.com/video/2023/12/04/194948-902196044_large.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
""", unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000/auth"

# Admin Login Form
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<div class="title">Admin Panel</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Superuser & Admin Login</div>', unsafe_allow_html=True)

admin_username = st.text_input("Admin Username", key="admin_username", value="SuperAdmin")
admin_password = st.text_input("Admin Password", type="password", key="admin_password", value="SuperSecurePassword")

if st.button("Login as Admin"):
    try:
        response = requests.post(f"{BACKEND_URL}/admin_login", json={
            "username": admin_username,
            "password": admin_password
        })
        if response.status_code == 200:
            st.success("Admin Login Successful! Redirecting...")
            # Set session state flag so the dashboard knows the admin is logged in.
            st.session_state.admin_logged_in = True
            st.switch_page("pages/admin_dashboard.py")
        elif response.status_code == 403:
            st.error("Access Denied: You are not an admin.")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")


st.markdown('</div>', unsafe_allow_html=True)

# Navigate Back to User Login Page
st.markdown('<a class="back-link" href="/pages/login">Back to User Login</a>', unsafe_allow_html=True)
