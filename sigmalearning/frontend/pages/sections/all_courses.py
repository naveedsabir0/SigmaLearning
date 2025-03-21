import streamlit as st
import requests
import random

def render_all_courses(courses):
    st.markdown('<div id="all-courses" class="section">', unsafe_allow_html=True)
    
    search_term = st.text_input("Search courses", key="course_search", placeholder="Type to search...")
    
    filtered_courses = courses
    if search_term:
        filtered_courses = [course for course in courses if search_term.lower() in course['title'].lower()]
    
    st.markdown("""  
    <style>
    .category-filter {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    .category-btn {
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid rgba(0, 255, 255, 0.4);
        color: #00FFFF;
        padding: 5px 15px;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .category-btn:hover {
        background: rgba(0, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    .course-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 25px;
        margin-top: 20px;
    }
    .course-card {
        position: relative;
        border-radius: 10px;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        height: 300px;
    }
    .course-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 255, 255, 0.2);
    }
    .course-card video {
        width: 100%;
        height: 60%;
        object-fit: cover;
        border-bottom: 1px solid rgba(0, 255, 255, 0.2);
    }
    .course-info {
        padding: 15px;
    }
    .course-title {
        color: #00FFFF;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .course-description {
        color: #EAEAEA;
        font-size: 14px;
        margin-bottom: 10px;
    }
    .course-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .course-difficulty {
        color: #FFA500;
        font-size: 12px;
    }
    .fav-button {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(0, 0, 0, 0.5);
        border: none;
        color: #FFF;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 10;
    }
    .fav-button:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: scale(1.1);
    }
    .fav-button.active {
        color: #FFD700;
    }
    .progress-bar {
        position: absolute;
        bottom: 0;
        left: 0;
        height: 3px;
        background: linear-gradient(90deg, #00FFFF 0%, #0066FF 100%);
        width: 0%;
        transition: width 0.5s ease;
    }
    .course-card:hover .progress-bar {
        width: 70%;
    }
    .course-action {
        text-align: center;
        margin-top: 10px;
        display: flex;
        justify-content: center;
        gap: 10px;
    }
    .download-btn {
        background: linear-gradient(90deg, #00FFFF 0%, #0066FF 100%);
        color: #000;
        border: none;
        padding: 5px 15px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .download-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    </style>
    <div class="category-filter">
        <div class="category-btn">All</div>
        <div class="category-btn">Programming</div>
        <div class="category-btn">Data Science</div>
        <div class="category-btn">AI</div>
        <div class="category-btn">Cybersecurity</div>
    </div>
    """, unsafe_allow_html=True)
    
    sample_descriptions = [
        "Master the fundamentals of Python programming with hands-on projects.",
        "Learn advanced data structures and algorithms for optimal problem-solving.",
        "Explore machine learning concepts and build your first AI models."
    ]
    
    difficulties = ["Beginner", "Advanced", "Intermediate"]
    
    st.markdown('<div class="course-grid">', unsafe_allow_html=True)
    for i, course in enumerate(filtered_courses):
        description = sample_descriptions[i % len(sample_descriptions)]
        difficulty = difficulties[i % len(difficulties)]
        is_favorite = course['id'] in st.session_state.get("favourites", [])
        fav_class = "active" if is_favorite else ""
        progress = random.randint(0, 100)
        
        card_html = f"""
        <div class="course-card" id="{course['id']}">
            <video autoplay muted loop playsinline>
                <source src="{course['video']}" type="video/mp4">
            </video>
            <button class="fav-button {fav_class}" id="fav-button-{course['id']}">★</button>
            <div class="course-info">
                <div class="course-title">{course['title']}</div>
                <div class="course-description">{description}</div>
                <div class="course-meta">
                    <div class="course-difficulty">{difficulty}</div>
                    <div class="course-duration">8 weeks</div>
                </div>
                <div class="course-action">
                    <button class="download-btn" id="download-button-{course['id']}">Download</button>
                </div>
            </div>
            <div class="progress-bar" style="width: {progress}%;"></div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        st.markdown(f"""
        <script>
            document.getElementById('fav-button-{course['id']}').addEventListener('click', function() {{
                document.getElementById('fav-{course['id']}').click();
            }});
            document.getElementById('download-button-{course['id']}').addEventListener('click', function() {{
                document.getElementById('download-{course['id']}').click();
            }});
        </script>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown(f"""
            <style>
                #fav-{course['id']} {{
                    display: none;
                }}
            </style>
            """, unsafe_allow_html=True)
            if st.button("★", key=f"fav-{course['id']}", help="Add to favorites"):
                if course['id'] in st.session_state.favourites:
                    st.session_state.favourites.remove(course['id'])
                else:
                    st.session_state.favourites.append(course['id'])
                st.rerun()
            
            st.markdown(f"""
            <style>
                #download-{course['id']} {{
                    display: none;
                }}
            </style>
            """, unsafe_allow_html=True)
            if st.button("Download", key=f"download-{course['id']}", help="Download course"):
                headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
                response = requests.get(f"http://127.0.0.1:5000/api/download_course/{course['id']}", headers=headers, stream=True)
                if response.status_code == 200:
                    file_bytes = response.content
                    st.download_button(
                        label="Click to Save Course",
                        data=file_bytes,
                        file_name=f"{course['title']}.mp4",
                        mime="video/mp4",
                        key=f"save-{course['id']}"
                    )
                else:
                    st.error(f"Failed to download course: {response.json().get('error', 'Unknown error')}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)