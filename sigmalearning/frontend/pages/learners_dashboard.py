import streamlit as st
import requests
import base64
from PIL import Image
import io
from pages.sections.my_profile import render_my_profile
from pages.sections.settings import render_settings
from pages.sections.all_courses import render_all_courses
from pages.sections.top_picks import render_top_picks
from pages.sections.favourites import render_favourites
from pages.sections.other_sections import render_other_sections

# Helper function to process and encode the uploaded image as WebP
def process_uploaded_image(uploaded_file):
    image = Image.open(uploaded_file)
    image = image.convert("RGB")
    image.thumbnail((300, 300))
    buffer = io.BytesIO()
    image.save(buffer, format="WEBP", quality=70)
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_image, image

# Check if user is logged in
if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
    st.error("Access denied. Please log in to view this page.")
    st.stop()

# Prevent access if email is not verified
if "email_verified" not in st.session_state or not st.session_state.email_verified:
    st.error("Your email is not verified. Please verify your email before accessing the dashboard.")
    st.stop()

username = st.session_state.get("username", "Learner")
just_registered = st.session_state.get("just_registered", False)

# Sample courses data (will be passed to relevant sections)
courses = [
    {"id": "course1", "title": "Introduction to Python", "video": "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"},
    {"id": "course2", "title": "Advanced Data Structures", "video": "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"},
    {"id": "course3", "title": "Machine Learning Basics", "video": "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"},
]

if "favourites" not in st.session_state:
    st.session_state["favourites"] = []

st.set_page_config(
    page_title="Learner Dashboard - SIGMA Learning",
    page_icon="📚",
    layout="wide",
)

# Inject custom CSS
st.markdown(
    """
    <style>
        /* Global Styles */
        body {
            background-color: #0a0a0a;
            color: white;
            margin: 0;
            padding: 0;
            font-family: 'Orbitron', sans-serif;
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
        /* Main Content Area */
        .main-content {
            margin-left: 300px;
            padding: 40px;
        }
        .header {
            text-align: left;
            margin-bottom: 40px;
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
        /* Section Styling */
        .section {
            padding: 20px;
            margin-bottom: 40px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            backdrop-filter: blur(5px);
        }
        .section h2 {
            font-size: 32px;
            margin-bottom: 20px;
        }
        /* Sidebar Navigation Styling */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        .sidebar-section {
            margin-bottom: 20px;
        }
        .sidebar-section h3 {
            font-size: 20px;
            color: #00FFFF;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            border-bottom: 1px solid #00D9FF;
            padding-bottom: 5px;
        }
        .nav-button {
            background: linear-gradient(45deg, #0070FF, #00D9FF);
            color: white;
            font-size: 18px;
            padding: 10px;
            border-radius: 8px;
            border: none;
            margin-bottom: 10px;
            text-transform: uppercase;
            transition: all 0.3s ease;
            width: 100%;
            cursor: pointer;
        }
        .nav-button:hover {
            background: linear-gradient(45deg, #00D9FF, #0070FF);
            transform: scale(1.05);
        }
        .nav-button-selected {
            background: linear-gradient(45deg, #0047AB, #00FFFF);
            box-shadow: 0 0 10px #00D9FF;
        }
        .logout-button {
            background: linear-gradient(45deg, #00D9FF, #0070FF);
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            text-transform: uppercase;
        }
        .logout-button:hover {
            background: linear-gradient(45deg, #0070FF, #00D9FF);
            transform: scale(1.05);
        }
    </style>
    <!-- Video Background -->
    <div class="video-background">
        <video autoplay loop muted playsinline>
            <source src="https://cdn.pixabay.com/video/2023/12/04/194948-902196044_large.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation
with st.sidebar:
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)
    st.markdown("<h1>SIGMA Platform</h1>", unsafe_allow_html=True)
    if "profile_pic" in st.session_state and st.session_state["profile_pic"]:
        profile_pic_b64 = st.session_state["profile_pic"]
        img_html = f'<img src="data:image/png;base64,{profile_pic_b64}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;">'
    else:
        img_html = '<i class="fas fa-user-circle" style="font-size:40px;"></i>'
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            {img_html}
            <p style="margin: 0 0 0 10px; font-size: 18px;">Hello, {username}</p>
        </div>
        """, unsafe_allow_html=True
    )

    # Initialize selected page in session state
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "My Profile"

    # Learning Section
    st.markdown('<div class="sidebar-section"><h3>Learning</h3></div>', unsafe_allow_html=True)
    learning_options = [
        "My Profile", "Settings", "All Courses", "Top Picks", "Favourites",
        "Progress", "Achievements", "Certificates", "Reviews",
        "Questions", "Help"
    ]
    for option in learning_options:
        is_selected = st.session_state.selected_page == option
        if st.button(option, key=f"learn_{option.lower().replace(' ', '_')}", 
                     help=option, 
                     use_container_width=True, 
                     args=({"class": f"nav-button{' nav-button-selected' if is_selected else ''}"},)):
            st.session_state.selected_page = option

    # Community Section
    st.markdown('<div class="sidebar-section"><h3>Community</h3></div>', unsafe_allow_html=True)
    community_options = ["My Feed", "My Notifications", "My Messages", "My Friends"]
    for option in community_options:
        is_selected = st.session_state.selected_page == option
        if st.button(option, key=f"comm_{option.lower().replace(' ', '_')}", 
                     help=option, 
                     use_container_width=True, 
                     args=({"class": f"nav-button{' nav-button-selected' if is_selected else ''}"},)):
            st.session_state.selected_page = option

    selected_page = st.session_state.selected_page

    st.write("")
    if st.button("Logout", key="sidebar_logout", help="Log out of your account"):
        st.session_state.pop("user_logged_in", None)
        st.switch_page("pages/login.py")  # Updated path

# Main Content Area
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="header">', unsafe_allow_html=True)
    welcome_message = "<p>Welcome! Your account has been successfully created.</p>" if just_registered else f"<p>Welcome back, {username}!</p>"
    st.markdown(f"<h1>{selected_page}</h1>{welcome_message}", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Render the selected section
    if selected_page == "My Profile":
        render_my_profile()
    elif selected_page == "Settings":
        render_settings()
    elif selected_page == "All Courses":
        render_all_courses(courses)
    elif selected_page == "Top Picks":
        render_top_picks()
    elif selected_page == "Favourites":
        render_favourites(courses)
    else:
        render_other_sections(selected_page)
    
st.markdown("</div>", unsafe_allow_html=True)