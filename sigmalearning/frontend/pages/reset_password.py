import streamlit as st
import requests

st.set_page_config(page_title="Reset Password - SIGMA Learning", page_icon="🔑")

# Custom CSS for styling consistency
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
    </style>
""", unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000/auth"

# --- Step 1: Request Password Reset Email ---
with st.form("request_reset_form"):
    st.markdown("### Request Password Reset")
    email = st.text_input("Enter your registered email", key="reset_email")
    request_submit = st.form_submit_button("Send Reset Link")
    if request_submit:
        try:
            response = requests.post(f"{BACKEND_URL}/forgot_password", json={"email": email})
            if response.status_code == 200:
                st.success("A password reset link has been sent to your email.")
            else:
                st.error(f"Error: {response.status_code} - {response.json().get('error', 'Request failed')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")

st.markdown("---")

# --- Step 2: Reset Password ---
with st.form("reset_password_form"):
    st.markdown("### Enter New Password")
    reset_token = st.text_input("Enter your reset token", key="reset_token")
    new_password = st.text_input("New Password", type="password", key="new_password")
    reset_submit = st.form_submit_button("Reset Password")
    if reset_submit:
        try:
            response = requests.post(f"{BACKEND_URL}/reset_password", json={"reset_token": reset_token, "password": new_password})
            if response.status_code == 200:
                st.success("Your password has been reset successfully! You can now log in.")
            else:
                st.error(f"Error: {response.status_code} - {response.json().get('error', 'Password reset failed')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")

# Navigate Back to Login Page
if st.button("Back to Login"):
    st.switch_page("pages/login.py")
