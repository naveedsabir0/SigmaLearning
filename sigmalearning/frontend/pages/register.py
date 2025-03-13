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

with st.form("register_form"):
    st.subheader("Register")
    reg_username = st.text_input("Username", key="reg_username")
    reg_email = st.text_input("Email", key="reg_email")
    reg_password = st.text_input("Password", type="password", key="reg_password")
    register_submit = st.form_submit_button("Register")

if register_submit:
    try:
        response = requests.post(f"{BACKEND_URL}/register", json={
            "username": reg_username,
            "email": reg_email,
            "password": reg_password
        })
        if response.status_code == 201:
            st.success(response.json().get("message", "Registration successful"))
            # Auto-login after registration
            login_resp = requests.post(f"{BACKEND_URL}/login", json={
                "username": reg_username,
                "password": reg_password
            })
            if login_resp.status_code == 200:
                login_data = login_resp.json()
                access_token = login_data["access_token"]
                st.session_state.user_logged_in = True
                st.session_state.access_token = access_token
                # Fetch user profile
                headers = {"Authorization": f"Bearer {access_token}"}
                profile_resp = requests.get("http://127.0.0.1:5000/api/user_profile", headers=headers)
                if profile_resp.status_code == 200:
                    profile_data = profile_resp.json()
                    st.session_state.user_id = profile_data["id"]
                    st.session_state.username = profile_data["username"]
                    st.session_state.email = profile_data["email"]
                    st.session_state.home_address = profile_data.get("home_address", "")
                    st.session_state.country = profile_data.get("country", "")
                    st.session_state.region = profile_data.get("region", "")
                    st.session_state.phone = profile_data.get("phone", "")
                    st.session_state.profile_pic = profile_data.get("profile_pic", "")
                st.switch_page("pages/learners_dashboard.py")
            else:
                st.error("Auto-login failed after registration")
        else:
            st.error(response.json().get("error", "Registration failed"))
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")

st.markdown("<hr>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("Already a member? Login", key="goto_login"):
        st.switch_page("pages/login.py")
with col2:
    if st.button("Admin Login", key="goto_admin"):
        st.switch_page("pages/adminlogin.py")
 