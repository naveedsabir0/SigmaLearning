import streamlit as st

# Remove Streamlit's default sidebar
st.set_page_config(page_title="SIGMA Learning - Welcome", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

# Inject custom CSS to completely remove the sidebar gap and add video background with futuristic fonts
st.markdown(f"""
    <style>
        /* Hide sidebar */
        [data-testid="stSidebarNav"], [data-testid="stSidebar"] {{
            display: none !important;
        }}

        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;700&family=Exo:wght@400;700&display=swap');

        body {{
            font-family: 'Exo', sans-serif;
            background-color: #121212;
            color: white;
            text-align: center;
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        
        .container {{
            text-align: center;
            max-width: 700px;
            margin: auto;
            position: relative;
            z-index: 1;
        }}
        
        .title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 48px;
            font-weight: 700;
            color: #00FFFF;
            text-align: center;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .subtitle {{
            font-family: 'Exo', sans-serif;
            font-size: 22px;
            font-weight: 300;
            color: #EAEAEA;
            text-align: center;
            margin-bottom: 40px;
        }}
        
        .button-container {{
            display: flex;
            justify-content: center;
            gap: 20px;
        }}
        
        .custom-button {{
            font-family: 'Rajdhani', sans-serif;
            background-color: #0070FF;
            border: none;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 15px 30px;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            width: 200px;
            text-align: center;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}

        .custom-button:hover {{
            background-color: #00D9FF;
            transform: scale(1.05);
        }}

        /* 🎥 Video Background */
        .video-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: -1;
        }}
        
        .video-container video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 0;
            left: 0;
            opacity: 0.6;
        }}
    </style>
    
    <div class="video-container">
        <video autoplay loop muted playsinline>
            <source src="https://cdn.pixabay.com/video/2023/12/04/194948-902196044_large.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
""", unsafe_allow_html=True)

# Content Container
st.markdown('<div class="container">', unsafe_allow_html=True)

st.markdown('<div class="title">SIGMA Learning Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Empowering digital education through innovation.</div>', unsafe_allow_html=True)

# Navigation Buttons
st.markdown('<div class="button-container">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Register"):
        st.switch_page("pages/register.py")  # Navigate to Register Page
with col2:
    if st.button("Login"):
        st.switch_page("pages/login.py")  # Navigate to Login Page

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
