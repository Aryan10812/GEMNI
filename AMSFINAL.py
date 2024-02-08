# Author - MrSentinel

import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
from dotenv import load_dotenv
from PIL import Image
import os
import io
import time

load_dotenv()

def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

st.image("./Google-Gemini-AI-Logo.png", width=200)
st.write("")

# Create a sidebar for history
if "history_pro" not in st.session_state:
    st.session_state.history_pro = []
if "history_vision" not in st.session_state:
    st.session_state.history_vision = []

# Display CHATAI text with rainbow color at the top
with st.sidebar:
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: -20px;">
            <h1 style="background: linear-gradient(to right, #FF0000, #FF7F00, #FFFF00, #00FF00, #0000FF, #4B0082, #8B00FF);
                        -webkit-background-clip: text;
                        color: transparent;
                        font-weight: bold;
                        font-size: 40px; margin-bottom: 0; padding-bottom: 0;">
                CHATAI
            </h1>
            <h1 style="font-size: 40px;"></h1>
        </div>
    """, unsafe_allow_html=True)

    gemini_mode = st.radio("Select Mode:", ["Gemini Pro", "Gemini Pro Vision"])

def gemini_pro_section():
    st.header("Interact with CHATAI")
    st.write("")

    # Use st.form to create a form
    with st.form(key='my_form'):
        prompt = st.text_input("Enter Your Question...", placeholder="Message To CHATAI...", label_visibility="visible", key="question_input")

        # Check if the form is submitted
        if st.form_submit_button("SEND"):
            with st.spinner("AI is thinking..."):
                st.session_state.history_pro.append(f"**User Input Question:** {prompt}")

                model_pro = genai.GenerativeModel("gemini-pro")
                response_pro = model_pro.generate_content(prompt)

                st.write("")
                st.header(":blue[Response]")
                st.write("")
                st.markdown(response_pro.text)

def gemini_vision_section():
    st.header("Interact with Gemini Pro Vision")
    st.write("")

    # Use st.form to create a form
    with st.form(key='vision_form'):
        image_prompt = st.text_input("Interact with the Image", placeholder="Prompt", label_visibility="visible", key="image_prompt_input")
        uploaded_file = st.file_uploader("Choose an Image", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp"])

        if uploaded_file is not None:
            st.image(Image.open(uploaded_file), use_column_width=True)
            st.markdown("""
                <style>
                    img {
                        border-radius: 10px;
                    }
                </style>
            """, unsafe_allow_html=True)

        # Check if the form is submitted
        if st.form_submit_button("GET RESPONSE"):
            with st.spinner("AI is thinking..."):
                model_vision = genai.GenerativeModel("gemini-pro-vision")

                if uploaded_file is not None:
                    if image_prompt != "":
                        image = Image.open(uploaded_file)

                        response_vision = model_vision.generate_content(
                            glm.Content(
                                parts=[
                                    glm.Part(text=image_prompt),
                                    glm.Part(
                                        inline_data=glm.Blob(
                                            mime_type="image/jpeg",
                                            data=image_to_byte_array(image)
                                        )
                                    )
                                ]
                            )
                        )

                        response_vision.resolve()

                        st.write("")
                        st.write(":blue[Response]")
                        st.write("")
                        st.markdown(response_vision.text)

                        # Add the user input question to the history
                        st.session_state.history_vision.append(f"**User Input Question:** {image_prompt}")

                        # Do not add the response to the history bar for the vision section

                    else:
                        st.write("")
                        st.header(":red[Please Provide a prompt]")

                else:
                    st.write("")
                    st.header(":red[Please Provide an image]")

def main():
    if gemini_mode == "Gemini Pro":
        gemini_pro_section()
    elif gemini_mode == "Gemini Pro Vision":
        gemini_vision_section()

# Display history in tabs
with st.sidebar:
    tabs = st.tabs(["History - Gemini Pro", "History - Gemini Pro Vision"])

    with tabs[0]:
        for item in st.session_state.history_pro:
            st.markdown(item)

    with tabs[1]:
        for item in st.session_state.history_vision:
            st.markdown(item)

# Move the input box to the bottom and make it fixed
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {position: fixed; bottom: 0; width: 100%; background-color: white; padding: 20px; box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);}
        .main {margin-bottom: 50px;}
    </style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
