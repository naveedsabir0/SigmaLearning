import streamlit as st

def render_top_picks():
    st.markdown('<div id="top-picks" class="section">', unsafe_allow_html=True)
    st.markdown("<h2>Top Picks</h2>", unsafe_allow_html=True)
    st.write("Based on your viewing history, here are some recommendations:")
    st.markdown("</div>", unsafe_allow_html=True)