import streamlit as st
import requests

def render_my_profile():
    st.markdown('<div id="my-profile" class="section">', unsafe_allow_html=True)
    st.markdown("<h2>My Profile Details</h2>", unsafe_allow_html=True)
    
    # --- Read-Only Username Field ---
    username = st.session_state.get("username", "Learner")
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
        from sigmalearning.frontend.pages.learners_dashboard import process_uploaded_image
        encoded_image, processed_image = process_uploaded_image(uploaded_pic)
        st.session_state["profile_pic"] = encoded_image
        st.image(processed_image, width=150)
        st.success("Profile picture updated!")
    
    # --- Remove Profile Picture Button ---
    if st.button("Remove Profile Picture", key="remove_profile_pic"):
        st.session_state["profile_pic"] = ""
        payload = {
            "email": st.session_state.get("email", ""),
            "home_address": st.session_state.get("home_address", ""),
            "country": st.session_state.get("country", ""),
            "city": st.session_state.get("city", ""),
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
        city_input = st.text_input("City", value=st.session_state.get("city", ""), key="city_input_form")
        region_input = st.text_input("Region", value=st.session_state.get("region", ""), key="region_input_form")
        phone_input = st.text_input("Phone Number", value=st.session_state.get("phone", ""), key="phone_input_form")
        
        submit_button = st.form_submit_button("Save Profile")
        
        if submit_button:
            payload = {
                "email": email_input,
                "home_address": address_input,
                "country": country_input,
                "city": city_input,
                "region": region_input,
                "phone": phone_input,
                "profile_pic": st.session_state.get("profile_pic", "")
            }
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            with st.spinner("Updating profile..."):
                try:
                    response = requests.put("http://127.0.0.1:5000/api/update_profile", json=payload, headers=headers)
                    if response.status_code == 200:
                        st.success("Profile updated successfully!")
                        profile_resp = requests.get("http://127.0.0.1:5000/api/user_profile", headers=headers)
                        if profile_resp.status_code == 200:
                            profile_data = profile_resp.json()
                            st.session_state["username"] = profile_data.get("username", username)
                            st.session_state["email"] = profile_data.get("email", "")
                            st.session_state["home_address"] = profile_data.get("home_address", "")
                            st.session_state["country"] = profile_data.get("country", "")
                            st.session_state["city"] = profile_data.get("city", "")
                            st.session_state["region"] = profile_data.get("region", "")
                            st.session_state["phone"] = profile_data.get("phone", "")
                            st.session_state["profile_pic"] = profile_data.get("profile_pic", "")
                        else:
                            st.error("Failed to refresh profile data.")
                    else:
                        st.error("Failed to update profile.")
                        st.error(f"Server response: {response.json().get('error', 'Unknown error')}")
                except Exception as e:
                    st.error("Error connecting to the backend.")
                    st.error(e)
    
    st.markdown("</div>", unsafe_allow_html=True)