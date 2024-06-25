from openai import OpenAI
import streamlit as st
from streamlit_option_menu import option_menu
import time
import toml
from streamlit_extras.bottom_container import bottom
from functions import *
import pandas as pd

# Retrieve the OpenAI API key
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]
OPENAI_KEY = st.secrets["OPENAI_KEY"]

client = OpenAI(api_key=OPENAI_KEY)

st.logo("https://moon.partners/mada/files/logo.png")
st.set_page_config(page_title="Mada - Vietnam Sourcing Advisor", page_icon=":speech_balloon:")

with st.sidebar:
    st.button('Watch Intro Video', on_click=show_popup)
    
    selected = option_menu(
        None, ["Sourcing", 'Procurement', 'Production', 'Exporting', 'About'], 
        icons=['1-square', '2-square', '3-square', '4-square', 'person'], 
        default_index=0, 
        styles={
            "nav-link-selected": {"background-color": "#31786b"}
            }
        )

if selected == 'Sourcing':
    file_url = None
    st.markdown("## Ask me anything about sourcing!")

    if "thread_id" not in st.session_state:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    if 'show_above' not in st.session_state:
        st.session_state.show_above = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    with bottom():

        above_container = st.empty()

        col1, col2 = st.columns([1, 12])
        with col1:
            st.button('🧷', on_click=show_upload)
        with col2:
            prompt = st.chat_input("Example: Where can I find 10,000 square meters of green hand made tiles?")
        
        if st.session_state.show_above == 'upload':
            if file_to_upload := above_container.file_uploader("Choose a file", key="uploaded_file"):
                file_url = ftp_upload(file_to_upload)
                # file_path = save_uploaded_file(uploaded_file)
                # file = client.files.create(
                #     file=open(file_path, "rb"),
                #     purpose="vision"
                #     )

    if prompt:
        
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)        

        content = [{'type': 'text', 'text': prompt}]
        if file_url:
            # content.append({'type': 'image_file', 'image_file': {"file_id": file.id}})
            content.append({'type': 'image_url', 'image_url': {"url": file_url}})

        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=content
        )
        
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=ASSISTANT_ID,
        )
        
        with st.spinner("Please wait while I look up that information for you."):
            while run.status != 'completed':
                time.sleep(0.5)
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id,
                    run_id=run.id
                )
                print(run.status)
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)

            last_reply = True

        # with above_container:
        #     col1, col2, col3 = st.columns([1, 1, 2])
        #     with col1:
        #         if st.button('Submit Order'): submit_order()
        #     with col2:
        #         if st.button('Download Report'): st.write('You have downloaded the report.')

        show_buttons()


    if st.session_state.show_above == 'buttons':
        with above_container:
            col1, col2, col3 = st.columns([3, 2, 4])
            with col1:
                if st.button('Connect with Suppliers'): submit_order()
            with col2:
                if st.button('Download Report'): st.toast('You have downloaded the report.', icon='✅')


    
if selected == 'Procurement':
    st.title("Procurement")

    st.markdown(
    """

    ## Streamlined Procurement Solutions

    Our procurement services are designed to simplify and optimize your procurement process, ensuring that you get the right materials at the right time.

    ### Our Procurement Process

    - **Material Planning**: We plan and manage your material requirements to ensure timely delivery.
    - **Order Management**: Our team handles order placement, tracking, and fulfillment.
    - **Inventory Management**: We manage your inventory levels to minimize stockouts and overstocking.

    ### Benefits

    - **Improved Efficiency**: Our procurement process reduces administrative burdens.
    - **Cost Savings**: We help you reduce costs through optimized procurement strategies.
    - **Enhanced Visibility**: Our system provides real-time visibility into your procurement process.

    ### Learn More

    Contact us to discuss how our procurement services can benefit your business.
    """
    )            

if selected == 'Production':
    st.title("Production")
    st.markdown(
        """

    ## Efficient Production Solutions

    Our production services are designed to optimize your manufacturing process, ensuring that you produce high-quality products efficiently and effectively.

    ### Our Production Process

    - **Production Planning**: We plan and manage your production schedule to ensure timely delivery.
    - **Quality Control**: Our team ensures that your products meet your quality standards.
    - **Inventory Management**: We manage your inventory levels to minimize stockouts and overstocking.

    ### Benefits

    - **Improved Efficiency**: Our production process reduces waste and minimizes downtime.
    - **Cost Savings**: We help you reduce costs through optimized production strategies.
    - **Enhanced Quality**: Our quality control process ensures that your products meet your quality standards.

    ### Learn More

    Contact us to discuss how our production services can benefit your business.
    """
    )

if selected == 'Exporting':
    st.title("Exporting")
    st.markdown(
        """

    ## Seamless Export Solutions

    Our exporting services are designed to simplify and optimize your export process, ensuring that your products reach global markets efficiently and effectively.

    ### Our Export Process

    - **Export Planning**: We plan and manage your export schedule to ensure timely delivery.
    - **Documentation**: Our team handles all necessary export documentation.
    - **Logistics**: We manage the logistics of exporting your products to global markets.

    ### Benefits

    - **Improved Efficiency**: Our export process reduces administrative burdens.
    - **Cost Savings**: We help you reduce costs through optimized export strategies.
    - **Enhanced Visibility**: Our system provides real-time visibility into your export process.

    ### Learn More

    Contact us to discuss how our exporting services can benefit your business.
    """
    )

if selected == 'About':
    st.title("About")
    st.markdown(
    """

    ## What We Do

    Mada is a supply chain management company dedicated to providing efficient and effective solutions for businesses. Our team of experts has years of experience in managing complex supply chains, ensuring timely delivery, and optimizing costs.

    ### Our Mission

    Our mission is to streamline your supply chain operations, enhance your customer experience, and drive business growth.

    ### Get in Touch

    Contact us to learn more about our services and how we can help your business thrive.

    **Los Angeles Office:**\\
    Moon Ho\\
    (323) 363-4734\\
    moon@chie.co

    **Vietnam Office**\\
    Tammy Vo\\
    +84 (0) 938 035 701\\
    hello@chie.co
    """
    )

print(st.session_state)