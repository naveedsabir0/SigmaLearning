import streamlit as st
import requests

# Check if admin is logged in; if not, show error and stop execution.
if 'admin_logged_in' not in st.session_state or not st.session_state.admin_logged_in:
    st.error("Access denied. Please log in as an admin to view this page.")
    st.stop()

st.set_page_config(page_title="Admin Dashboard - SIGMA Learning", page_icon="🚀", layout="wide")

# Futuristic custom CSS with video background
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
        body {
            font-family: 'Orbitron', sans-serif;
            background-color: #0a0a0a;
            color: white;
            margin: 0;
            padding: 0;
        }
        .header {
            text-align: center;
            padding: 30px;
        }
        .header h1 {
            font-size: 48px;
            color: #00FFFF;
            margin-bottom: 10px;
        }
        .header p {
            font-size: 24px;
            color: #EAEAEA;
        }
        .nav {
            display: flex;
            justify-content: center;
            gap: 30px;
            padding: 20px;
        }
        .nav a {
            text-decoration: none;
            color: #00D9FF;
            font-size: 20px;
            transition: color 0.3s ease;
        }
        .nav a:hover {
            color: #0070FF;
        }
        .section {
            padding: 20px;
            margin: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            backdrop-filter: blur(5px);
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

# Header Section
st.markdown("""
    <div class="header">
        <h1>Admin Dashboard</h1>
        <p>Welcome, SuperAdmin</p>
    </div>
""", unsafe_allow_html=True)

# Navigation Bar
st.markdown("""
    <div class="nav">
        <a href="#overview">Overview</a>
        <a href="#users">Manage Users</a>
        <a href="#feedback">View Feedback</a>
        <a href="#settings">Settings</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .logout-button {
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
        .logout-button:hover {
            background: linear-gradient(45deg, #0070FF, #00D9FF);
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

if st.button("Logout"):
    # Remove the admin_logged_in flag from session state
    st.session_state.pop("admin_logged_in", None)
    # Redirect to the admin login page
    st.switch_page("pages/adminlogin.py")

# Overview Section
st.markdown('<div id="overview" class="section">', unsafe_allow_html=True)
st.subheader("Overview")
st.write("Quick summary of platform metrics:")
st.write("Total Users: 100")
st.write("Total Feedbacks: 25")
st.markdown('</div>', unsafe_allow_html=True)

# Manage Users Section
st.markdown('<div id="users" class="section">', unsafe_allow_html=True)
st.subheader("Manage Users")
try:
    response = requests.get("http://127.0.0.1:5000/api/users")
    if response.status_code == 200:
        users = response.json()
        st.write("User List:")
        for user in users:
            st.write(f"ID: {user['id']} | Username: {user['username']} | Email: {user['email']}")
    else:
        st.error("Failed to fetch users.")
except Exception as e:
    st.error(f"Error fetching users: {e}")
st.markdown('</div>', unsafe_allow_html=True)

# Feedback Section
st.markdown('<div id="feedback" class="section">', unsafe_allow_html=True)
st.subheader("View Feedback")
st.write("Feedback functionality coming soon.")
st.markdown('</div>', unsafe_allow_html=True)

# Settings Section
st.markdown('<div id="settings" class="section">', unsafe_allow_html=True)
st.subheader("Settings")
st.write("Settings options will be available here.")
st.markdown('</div>', unsafe_allow_html=True)
