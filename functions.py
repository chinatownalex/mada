import os
import streamlit as st

def show_upload():
    if st.session_state.show_above != 'upload':
        st.session_state.show_above = 'upload'
    elif st.session_state.show_above == 'upload':
        st.session_state.show_above = None

def show_buttons():
    if st.session_state.show_above != 'buttons':
        st.session_state.show_above = 'buttons'
    elif st.session_state.show_above == 'buttons':
        st.session_state.show_above = None

def save_uploaded_file(uploaded_file):
    # Define the file path
    file_path = os.path.join("files", uploaded_file.name)
    
    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

@st.experimental_dialog('Connect with Suppliers')
def submit_order():
    with st.form("connect"):
        st.write("Please fill in your order detail and 5 suppliers will contact you shortly.")
        name = st.text_input("Name")
        email = st.text_input("Email")
        description = st.text_area("Order description")
        file = st.file_uploader("Upload file")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(f"Thanks for your order {name}. We'll send you an {email}")
