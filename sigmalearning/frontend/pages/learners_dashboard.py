import streamlit as st
import requests

# Check if user is logged in; if not, show error and stop execution.
if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
    st.error("Access denied. Please log in to view this page.")
    st.stop()

# For demo purposes, assume the username is stored in session_state
username = st.session_state.get("username", "Learner")
# Flag to indicate a recent registration
just_registered = st.session_state.get("just_registered", False)

# Sample courses data (in a real app this would come from the backend)
courses = [
    {
        "id": "course1",
        "title": "Introduction to Python",
        "video": "https://samplelib.com/lib/preview/mp4/sample-5s.mp4",
    },
    {
        "id": "course2",
        "title": "Advanced Data Structures",
        "video": "https://samplelib.com/lib/preview/mp4/sample-5s.mp4",
    },
    {
        "id": "course3",
        "title": "Machine Learning Basics",
        "video": "https://samplelib.com/lib/preview/mp4/sample-5s.mp4",
    },
]

# Initialize favourites in session state if not already set.
if "favourites" not in st.session_state:
    st.session_state["favourites"] = []

# Set page config (leaving the default sidebar visible)
st.set_page_config(
    page_title="Learner Dashboard - SIGMA Learning",
    page_icon="📚",
    layout="wide",
)

# Inject custom CSS (without hiding the default sidebar container but hiding its extra pages)
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

        /* Course Card Styling */
        .course-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        .course-card {
            position: relative;
            overflow: hidden;
            border-radius: 10px;
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        .course-card:hover {
            transform: scale(1.02);
        }
        .course-card video {
            width: 100%;
            height: 140px;
            object-fit: cover;
            transition: opacity 0.3s ease;
            opacity: 0;
        }
        .course-card:hover video {
            opacity: 1;
        }
        .course-card .course-title {
            padding: 10px;
            background: rgba(0,0,0,0.6);
            position: absolute;
            bottom: 0;
            width: 100%;
            font-size: 18px;
            text-align: center;
        }
        .course-card .fav-button {
            position: absolute;
            top: 10px;
            right: 10px;
            background: transparent;
            border: none;
            color: #00D9FF;
            font-size: 18px;
            cursor: pointer;
            transition: color 0.3s ease;
        }
        .course-card .fav-button:hover {
            color: #0070FF;
        }

        /* Custom Sidebar Navigation Styling */
        /* Hide the automatically generated pages from the sidebar */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        /* Styling for our custom sidebar links */
        [data-testid="stSidebar"] a {
            color: #fff !important;
            text-decoration: none !important;
            font-size: 18px;
            margin-bottom: 10px;
            display: block;
            padding: 10px 15px;
            text-transform: uppercase;
        }
        [data-testid="stSidebar"] a:hover {
            background-color: rgba(255, 255, 255, 0.1);
            color: #fff !important;
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

# Update the default sidebar with only Learner Dashboard–related navigation and a Logout button
with st.sidebar:
    st.markdown("<h1>SIGMA Learning</h>", unsafe_allow_html=True)
    st.markdown(
        """
        <nav>
            <hr>
            <a href="#my-profile">My Profile</a>
            <a href="#settings">Settings</a>
            <a href="#all-courses">All Courses</a>
            <a href="#top-picks">Top Picks</a>
            <a href="#favourites">Favourites</a>
            <a href="#my-progress">My Progress</a>
            <a href="#my-achievements">My Achievements</a>
            <a href="#my-certificates">My Certificates</a>
            <a href="#my-reviews">My Reviews</a>
            <a href="#my-questions">My Questions</a>
            <a href="#my-notifications">My Notifications</a>
            <a href="#my-messages">My Messages</a>
            <a href="#my-friends">My Friends</a>
            <a href="#help">Help</a>
        </nav>
        """,
        unsafe_allow_html=True,
    )
    st.write("")  # spacer
    if st.button("Logout", key="sidebar_logout"):
        st.session_state.pop("user_logged_in", None)
        st.switch_page("pages/login.py")

# Main Content Area
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    # Header Message
    st.markdown('<div class="header">', unsafe_allow_html=True)
    if just_registered:
        welcome_message = "<p>Welcome! Your account has been successfully created.</p>"
    else:
        welcome_message = f"<p>Welcome back, {username}!</p>"
    st.markdown(f"<h1>Learner Dashboard</h1>{welcome_message}", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Section 1: All Courses
    st.markdown('<div id="all-courses" class="section">', unsafe_allow_html=True)
    st.markdown("<h2>All Courses</h2>", unsafe_allow_html=True)

    # Display courses in a grid
    st.markdown('<div class="course-grid">', unsafe_allow_html=True)
    for course in courses:
        card_html = f"""
            <div class="course-card">
                <video muted loop playsinline>
                    <source src="{course['video']}" type="video/mp4">
                </video>
                <div class="course-title">{course['title']}</div>
                <button class="fav-button" onclick="window.location.href='?fav={course['id']}'">★</button>
            </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Process favouriting via query parameters (simulate adding to favourites)
    query_params = st.query_params
    fav_id = query_params.get("fav", [None])[0]
    if fav_id and fav_id not in st.session_state.favourites:
        st.session_state.favourites.append(fav_id)
        st.set_query_params()  # Clear query parameters

    # Section 2: Top Picks
    st.markdown('<div id="top-picks" class="section">', unsafe_allow_html=True)
    st.markdown("<h2>Top Picks</h2>", unsafe_allow_html=True)
    st.write("Based on your viewing history, here are some recommendations:")
    st.markdown("</div>", unsafe_allow_html=True)

    # Section 3: Favourites
    st.markdown('<div id="favourites" class="section">', unsafe_allow_html=True)
    st.markdown("<h2>Favourites</h2>", unsafe_allow_html=True)
    if st.session_state.favourites:
        st.write("Your favourited courses:")
        # Filter courses that are favourited (for demo, match by course id)
        fav_courses = [course for course in courses if course["id"] in st.session_state.favourites]
        st.markdown('<div class="course-grid">', unsafe_allow_html=True)
        for course in fav_courses:
            card_html = f"""
                <div class="course-card">
                    <video muted loop playsinline>
                        <source src="{course['video']}" type="video/mp4">
                    </video>
                    <div class="course-title">{course['title']}</div>
                    <div style="position:absolute; bottom:10px; left:10px; background:rgba(0,0,0,0.6); padding:5px; border-radius:5px;">
                        Progress: 50%
                    </div>
                </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.write("You have no favourites yet.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
