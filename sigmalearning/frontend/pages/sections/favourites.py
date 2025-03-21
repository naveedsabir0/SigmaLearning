import streamlit as st

def render_favourites(courses):
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