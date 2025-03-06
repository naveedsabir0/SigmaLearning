import streamlit as st
import requests
from sigmalearning.frontend.helpers import translate_text

st.title("🌍 Digital Literacy App")

# Language Selection
language = st.selectbox("Choose Language", ["English", "French", "Spanish", "Swahili"])
lang_codes = {"English": "en", "French": "fr", "Spanish": "es", "Swahili": "sw"}
target_lang = lang_codes[language]

# Fetch Users
response = requests.get("http://127.0.0.1:5000/users")
if response.status_code == 200:
    users = response.json()
    for user in users:
        name = translate_text(user[1], target_lang)
        email = user[2]
        literacy_level = translate_text(user[3], target_lang)
        st.write(f"**Name:** {name}, **Email:** {email}, **Level:** {literacy_level}")
else:
    st.error("Failed to load users.")

# Feedback Submission
st.subheader("📝 Submit Feedback")
user_id = st.number_input("User ID", min_value=1)
comments = st.text_area("Your Feedback")
if st.button("Submit"):
    feedback_data = {"user_id": user_id, "comments": comments}
    response = requests.post("http://127.0.0.1:5000/add_feedback", json=feedback_data)
    if response.status_code == 200:
        st.success("Feedback submitted successfully!")
    else:
        st.error("Error submitting feedback.")
