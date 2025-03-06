import streamlit as st
import requests

# Check if user is logged in; if not, show error and stop execution.
if 'user_logged_in' not in st.session_state or not st.session_state.user_logged_in:
    st.error("Access denied. Please log in to view this page.")
    st.stop()

st.set_page_config(page_title="Learner Dashboard - SIGMA Learning", page_icon="📚", layout="wide")

# Futuristic custom CSS with video background (matches the other pages)
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
        <h1>Learner Dashboard</h1>
        <p>Welcome to SIGMA Learning Platform</p>
    </div>
""", unsafe_allow_html=True)

# Navigation Bar
st.markdown("""
    <div class="nav">
        <a href="#overview">Overview</a>
        <a href="#courses">My Courses</a>
        <a href="#progress">Progress</a>
        <a href="#feedback">Feedback</a>
    </div>
""", unsafe_allow_html=True)

# Logout Button (Styled like the rest of the buttons)
if st.button("Logout", key="logout"):
    st.session_state.pop("user_logged_in", None)
    st.switch_page("pages/login.py")  # Assuming "login" is the registered name for login.py

# Overview Section
st.markdown('<div id="overview" class="section">', unsafe_allow_html=True)
st.subheader("Overview")
st.write("Here's a summary of your learning journey and latest updates.")
st.markdown('</div>', unsafe_allow_html=True)

# My Courses Section
st.markdown('<div id="courses" class="section">', unsafe_allow_html=True)
st.subheader("My Courses")
st.write("List of enrolled courses will appear here.")
st.markdown('</div>', unsafe_allow_html=True)

# Progress Section
st.markdown('<div id="progress" class="section">', unsafe_allow_html=True)
st.subheader("Progress")
st.write("Your learning progress, milestones, and achievements will be displayed here.")
st.markdown('</div>', unsafe_allow_html=True)

# Feedback Section
st.markdown('<div id="feedback" class="section">', unsafe_allow_html=True)
st.subheader("Feedback")
st.write("View feedback on your courses and provide your own insights.")
st.markdown('</div>', unsafe_allow_html=True)
