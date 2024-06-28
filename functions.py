import os
import streamlit as st
from ftplib import FTP

@st.experimental_dialog("Mada - Vietnam Sourcing Advisor", width="large")
def show_popup():
    video_url = 'https://moon.partners/mada/files/intro_video.mp4'
    st.video(video_url)

def download_report(message):
    markdown_logo = f'![Mada Logo](https://moon.partners/mada/files/logo.png)'
    markdownl_title = f"# Mada Sourcing Report"
    markdown_content = message['content']
    line_break = '\n'
    html_content = markdown.markdown(markdown_logo + line_break  + markdownl_title + line_break + markdown_content)

    HTML(string=html_content).write_pdf('mada_sourcing_report.pdf')

    
def ftp_upload(file):
    try:
        # Connect to the FTP server
        ftp = FTP('ftp.moon.partners')
        ftp.login(user='mada@moon.partners', passwd='Buffdude22!')

        # Change to the desired directory on the FTP server
        ftp.cwd('uploads/')

        # Open the local CSV file in binary mode
        # with open(local_path + filename, 'rb') as file:
            # Upload the file to the FTP server
        ftp.storbinary('STOR ' + file.name, file)

        print(f'{file.name} uploaded successfully')
        
    except Exception as e:
        print('Error occurred:', e)
        
    finally:
        # Close the FTP connection
        ftp.quit()

    file_url = f'https://moon.partners/mada/uploads/{file.name}'

    return file_url


def toggle_upload():
    if st.session_state.show_above == 'upload':
        st.session_state.show_above = None
        st.session_state.uploaded_file = None
    elif st.session_state.show_above != 'upload':
        st.session_state.show_above = 'upload'

# def clear_upload():
#     st.session_state.uploaded_file = None
#     st.session_state.show_above = None
        
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
