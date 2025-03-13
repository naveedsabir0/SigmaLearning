import streamlit as st
import requests
import base64
from PIL import Image
import io

# Check if user is logged in; if not, show error and stop execution.
if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
    st.error("Access denied. Please log in to view this page.")
    st.stop()

username = st.session_state.get("username", "Learner")
just_registered = st.session_state.get("just_registered", False)

# Sample courses data (in a real app this would come from the backend)
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

# Inject custom CSS (styling remains unchanged)
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
        [data-testid="stSidebar"] a, .nav-link {
            color: #fff !important;
            text-decoration: none !important;
            font-size: 18px;
            margin-bottom: 10px;
            display: block;
            padding: 10px 15px;
            text-transform: uppercase;
        }
        [data-testid="stSidebar"] a:hover, .nav-link:hover {
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

# ---------------------------
# Sidebar Navigation (unchanged)
# ---------------------------
with st.sidebar:
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)
    st.markdown("<h1>SIGMA Learning</h1>", unsafe_allow_html=True)
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
    
    nav_options = [
        "My Profile", "Settings", "All Courses", "Top Picks", "Favourites",
        "My Progress", "My Achievements", "My Certificates", "My Reviews",
        "My Questions", "My Notifications", "My Messages", "My Friends", "Help"
    ]
    
    selected_page = st.radio("Navigation", nav_options, index=0, key="nav_selection")
    st.write("")
    if st.button("Logout", key="sidebar_logout"):
        st.session_state.pop("user_logged_in", None)
        st.switch_page("pages/login.py")

# ---------------------------
# Main Content Area (unchanged except for "My Profile")
# ---------------------------
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="header">', unsafe_allow_html=True)
    welcome_message = "<p>Welcome! Your account has been successfully created.</p>" if just_registered else f"<p>Welcome back, {username}!</p>"
    st.markdown(f"<h1>{selected_page}</h1>{welcome_message}", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if selected_page == "My Profile":
        st.markdown('<div id="my-profile" class="section">', unsafe_allow_html=True)
        st.markdown("<h2>My Profile Details</h2>", unsafe_allow_html=True)
        
        # --- Read-Only Username Field ---
        st.text_input("Username", value=username, key="username_display", disabled=True)
        
        # --- Profile Picture Section ---
        st.markdown("**Current Profile Picture:**")
        if "profile_pic" in st.session_state and st.session_state["profile_pic"]:
            st.image("data:image/png;base64," + st.session_state["profile_pic"], width=150)
        else:
            st.write("No profile picture available.")
        st.markdown("**Upload a New Profile Picture:**")
        uploaded_pic = st.file_uploader("Select an image", type=["png", "jpg", "jpeg"], key="profile_pic_upload")
        if uploaded_pic is not None:
            # Use Pillow to open, resize, and compress the image
            image = Image.open(uploaded_pic)
            image.thumbnail((300, 300))
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=70)
            encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
            st.session_state["profile_pic"] = encoded_image
            st.image(image, width=150)
            st.success("Profile picture updated!")
        
        # --- Remove Profile Picture Button ---
        if st.button("Remove Profile Picture", key="remove_profile_pic"):
            st.session_state["profile_pic"] = ""
            payload = {
                "email": st.session_state.get("email", ""),
                "home_address": st.session_state.get("home_address", ""),
                "country": st.session_state.get("country", ""),
                "region": st.session_state.get("region", ""),
                "phone": st.session_state.get("phone", ""),
                "profile_pic": ""
            }
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            try:
                response = requests.put("http://127.0.0.1:5000/api/update_profile", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Profile picture removed successfully!")
                else:
                    st.error(f"Failed to remove profile picture: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error connecting to the backend: {e}")
        
        # --- Profile Input Fields in a Form ---
        with st.form("profile_form"):
            email_input = st.text_input("Email Address", value=st.session_state.get("email", ""), key="email_input_form")
            address_input = st.text_input("Home Address", value=st.session_state.get("home_address", ""), key="address_input_form")
            country_input = st.text_input("Country", value=st.session_state.get("country", ""), key="country_input_form")
            region_input = st.text_input("Region", value=st.session_state.get("region", ""), key="region_input_form")
            phone_input = st.text_input("Phone Number", value=st.session_state.get("phone", ""), key="phone_input_form")
            
            submit_button = st.form_submit_button("Save Profile")
            
            if submit_button:
                payload = {
                    "email": email_input,
                    "home_address": address_input,
                    "country": country_input,
                    "region": region_input,
                    "phone": phone_input,
                    "profile_pic": st.session_state.get("profile_pic", "")
                }
                headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
                try:
                    response = requests.put("http://127.0.0.1:5000/api/update_profile", json=payload, headers=headers)
                    if response.status_code == 200:
                        st.success("Profile updated successfully!")
                        # Refresh the user profile from the backend:
                        profile_resp = requests.get("http://127.0.0.1:5000/api/user_profile", headers=headers)
                        if profile_resp.status_code == 200:
                            profile_data = profile_resp.json()
                            st.session_state["username"] = profile_data.get("username", username)
                            st.session_state["email"] = profile_data.get("email", "")
                            st.session_state["home_address"] = profile_data.get("home_address", "")
                            st.session_state["country"] = profile_data.get("country", "")
                            st.session_state["region"] = profile_data.get("region", "")
                            st.session_state["phone"] = profile_data.get("phone", "")
                            st.session_state["profile_pic"] = profile_data.get("profile_pic", "")
                            username = st.session_state["username"]
                        else:
                            st.error("Failed to refresh profile data.")
                    else:
                        st.error("Failed to update profile.")
                        st.error(f"Server response: {response.json().get('error', 'Unknown error')}")
                except Exception as e:
                    st.error("Error connecting to the backend.")
                    st.error(e)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif selected_page == "Settings":
        st.markdown('<div id="settings" class="section">', unsafe_allow_html=True)
        st.markdown("<h2>Settings</h2>", unsafe_allow_html=True)
        st.write("Settings content goes here.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif selected_page == "All Courses":
        st.markdown('<div id="all-courses" class="section">', unsafe_allow_html=True)
        st.markdown("<h2>All Courses</h2>", unsafe_allow_html=True)
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
    
    elif selected_page == "Top Picks":
        st.markdown('<div id="top-picks" class="section">', unsafe_allow_html=True)
        st.markdown("<h2>Top Picks</h2>", unsafe_allow_html=True)
        st.write("Based on your viewing history, here are some recommendations:")
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif selected_page == "Favourites":
        st.markdown('<div id="favourites" class="section">', unsafe_allow_html=True)
        st.markdown("<h2>Favourites</h2>", unsafe_allow_html=True)
        if st.session_state.favourites:
            st.write("Your favourited courses:")
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
    
    else:
        st.write("Content for selected page goes here.")
    
    st.markdown("</div>", unsafe_allow_html=True)
