import streamlit as st
import requests

def render_settings():
    st.markdown('<div id="settings" class="section">', unsafe_allow_html=True)
    st.markdown("<h2>Settings</h2>", unsafe_allow_html=True)
    
    st.markdown("### Two-Factor Authentication (2FA)")
    st.write("Enhance your account security by activating 2FA. Enter your phone number below to receive a 6-digit activation code.")
    
    with st.form("activate_2fa_form"):
        phone_input = st.text_input("Phone Number", value=st.session_state.get("phone", ""), key="phone_input")
        send_code = st.form_submit_button("Send Activation Code")
        if send_code:
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            payload = {"phone": phone_input}
            response = requests.post("http://127.0.0.1:5000/auth/activate_2fa", json=payload, headers=headers)
            if response.status_code == 200:
                st.success("Activation code sent to your phone.")
            else:
                st.error(f"Error: {response.json().get('error', 'Failed to send activation code')}")
    
    st.write("Once you receive the code, enter it below to activate 2FA:")
    
    with st.form("verify_2fa_activation_form"):
        activation_code = st.text_input("Activation Code", key="activation_code")
        verify_activation = st.form_submit_button("Activate 2FA")
        if verify_activation:
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            payload = {"activation_code": activation_code}
            response = requests.post("http://127.0.0.1:5000/auth/verify_2fa_activation", json=payload, headers=headers)
            if response.status_code == 200:
                st.success("2FA activated successfully!")
            else:
                st.error(f"Error: {response.json().get('error', 'Failed to activate 2FA')}")
    
    st.markdown("### 2FA Toggle")
    current_2fa = st.session_state.get("two_fa_enabled", False)
    new_2fa = st.checkbox("Enable Two-Factor Authentication", value=current_2fa, key="toggle_2fa")
    
    if new_2fa != current_2fa:
        with st.expander("Confirm 2FA Change", expanded=True):
            st.write("Please enter your password to confirm this change.")
            password_input = st.text_input("Password", type="password", key="confirm_2fa_password")
            confirm_button = st.button("Confirm 2FA Change", key="confirm_2fa_change")
            if confirm_button:
                headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
                payload = {"password": password_input, "two_fa_enabled": new_2fa}
                response = requests.post("http://127.0.0.1:5000/auth/update_2fa_setting", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("2FA setting updated successfully!")
                    st.session_state["two_fa_enabled"] = new_2fa
                else:
                    st.error(f"Error: {response.json().get('error', 'Failed to update 2FA setting')}")
    
    st.markdown("</div>", unsafe_allow_html=True)