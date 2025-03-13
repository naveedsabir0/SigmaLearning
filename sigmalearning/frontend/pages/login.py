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
        .nav-button-container button {
            width: 220px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000/auth"

# Display title outside the form
st.title("SIGMA Learning Platform")

# Login form (centered)
with st.form("login_form"):
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    submit = st.form_submit_button("Login")
    
    if submit:
        try:
            response = requests.post(f"{BACKEND_URL}/login", json={
                "username": login_username,
                "password": login_password
            })
            if response.status_code == 200:
                data = response.json()
                access_token = data["access_token"]
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
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")

st.markdown("<hr>", unsafe_allow_html=True)

# Navigation buttons in three equal columns with a large gap.
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    with st.container():
        st.markdown('<div class="nav-button-container" style="width:220px; margin:auto;">', unsafe_allow_html=True)
        if st.button("Forgot your password? Reset it here", key="goto_reset"):
            st.switch_page("pages/reset_password.py")
        st.markdown('</div>', unsafe_allow_html=True)
with col2:
    with st.container():
        st.markdown('<div class="nav-button-container" style="width:220px; margin:auto;">', unsafe_allow_html=True)
        if st.button("Don\'t have an account? Register here", key="goto_register"):
            st.switch_page("pages/register.py")
        st.markdown('</div>', unsafe_allow_html=True)
with col3:
    with st.container():
        st.markdown('<div class="nav-button-container" style="width:220px; margin:auto;">', unsafe_allow_html=True)
        if st.button("Admin Login", key="goto_admin"):
            st.switch_page("pages/adminlogin.py")
        st.markdown('</div>', unsafe_allow_html=True)
