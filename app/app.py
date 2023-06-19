import streamlit as st
import io
import requests
from PIL import Image, ImageOps, ImageDraw
import base64
import streamlit as st
from PIL import Image, ImageDraw
import io
import base64
import requests
import json
from PIL import Image
import openai
import os
from openai import cli
import matplotlib.pyplot as plt
import azure.ai.vision as visionsdk
from io import BytesIO
import time
from function import *

# Set up the canvas size and initial position of the images
canvas_width = 1024
canvas_height = 1024
image_size = 500
image_x = (canvas_width - image_size) // 2
image_y = (canvas_height - image_size) // 2

openai.api_type = "open_ai"
openai.api_base = 'https://api.openai.com/v1'
openai.api_version = None



def main():
    
    with st.sidebar:
        radio = st.radio(
            "What kind of image transformation magic would you like to see today?",
            ("Alter background", "Modify background with editing", "Create portrait using your own photo"))
        st.markdown(
                """<style>
                div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
                    font-size: 20px;
                }
                    </style>
                    """, unsafe_allow_html=True)

    if radio == 'Modify background with editing':
        st.title("Modify background with editing")
        azure_vision_endpoint = st.text_input('Azure Computer Vision Endpoint')  # added this line
        azure_vision = st.text_input('Azure Computer Vision API Key')  # added this line
        organization = st.text_input('OpenAI Organization')
        api_key = st.text_input('OpenAI API Key')
        openai.api_key=api_key
        openai.organization=organization
        uploaded_front = st.file_uploader("Upload the front image...", type=["jpg", "jpeg", "png"])
        uploaded_back = st.text_input("Enter text:", value= "a room, Domestic interiors")


        if uploaded_front is not None and uploaded_back is not None:
            front_image = load_images(uploaded_front,azure_vision,azure_vision_endpoint)

            canvas_width = 1024
            canvas_height = 1024
            image_size = 500
            image_x = (canvas_width - image_size) // 2
            image_y = (canvas_height - image_size) // 2
            with st.sidebar:
                front_width = st.slider("Set the width of the front image:", min_value=50, max_value=2000, value=image_size, step=10)
                new_x_front = st.slider("Move the front image horizontally:", min_value=0, max_value=canvas_width, value=200, step=10)
                new_y_front = st.slider("Move the front image vertically:", min_value=0, max_value=canvas_height, value=200, step=10)
            
            back_width=1024
            front_height = display_images(front_image, front_width)
            canvas_image,new_front = move_images(front_image, front_width, front_height, new_x_front, new_y_front,canvas_width, canvas_height)

            if st.button("Generate Image"):
                new_image=dalle_edit(new_front,uploaded_back)

                # Display the canvas_image using streamlit
                st.image(new_image, use_column_width=False, width=canvas_width)



                # Convert the image url to a PIL image
                response = requests.get(new_image)
                image = Image.open(BytesIO(response.content))
                
                # Save the image as a PNG file
                with BytesIO() as output:
                    image.save(output, format="PNG")
                    png_data = output.getvalue()
                print(len(png_data))   
                # Download the PNG file
                b64 = base64.b64encode(png_data).decode()
                href = f'<a href="data:file/png;base64,{b64}" download="image.png" style="font-size: 20px;">Download PNG file</a>'

                
                st.markdown(href, unsafe_allow_html=True)

    elif radio == "Alter background":


        st.title("Alter background")
        azure_vision_endpoint = st.text_input('Azure Computer Vision Endpoint')  # added this line
        azure_vision = st.text_input('Azure Computer Vision API Key')  # added this line
        organization = st.text_input('OpenAI Organization')
        api_key = st.text_input('OpenAI API Key')
        openai.api_key=api_key
        openai.organization=organization


        uploaded_front = st.file_uploader("Upload the front image...", type=["jpg", "jpeg", "png"])
        uploaded_back = st.text_input("Enter text:", value="wooden city, Daguerrotype")

        if len(uploaded_back) < 1:
            uploaded_back = None

        # Check if images already exist in session state
        if "front_image" not in st.session_state or "back_image" not in st.session_state:
            st.session_state.front_image = None
            st.session_state.back_image = None

        front_image, back_image = st.session_state.front_image, st.session_state.back_image

        if st.button("Get Background Image") and uploaded_front is not None and uploaded_back is not None:
            # Load images if not already loaded
            if front_image is None or back_image is None:
                front_image, back_image = load_images1(uploaded_front, uploaded_back,azure_vision,azure_vision_endpoint)
                st.session_state.front_image = front_image
                st.session_state.back_image = back_image

        # Rest of your code that is not affected by slider values
        if st.session_state.front_image is not None and st.session_state.back_image is not None:
            canvas_width, canvas_height = 1024, 1024
            front_width, back_width, new_x_front, new_y_front = 200, 1024, 200, 200

            with st.sidebar:
                front_width = st.slider("Set the width of the front image:", min_value=50, max_value=2000, value=front_width, step=10)
                back_width = st.slider("Set the width of the back image:", min_value=50, max_value=1024, value=back_width, step=10)
                new_x_front = st.slider("Move the front image horizontally:", min_value=0, max_value=canvas_width, value=new_x_front, step=10)
                new_y_front = st.slider("Move the front image vertically:", min_value=0, max_value=canvas_height, value=new_y_front, step=10)

            front_height = display_images1(st.session_state.front_image, st.session_state.back_image, front_width, back_width)
            canvas_image = move_images2(st.session_state.front_image, st.session_state.back_image, front_width, back_width, front_height, new_x_front, new_y_front,canvas_width, canvas_height)

            save_image(canvas_image)

            st.button("Clear Images", on_click=clear_session_state)


    elif radio == "Create portrait using your own photo":
        st.title("Create portrait using your own photo")
        canvas_width = 1024
        canvas_height = 1024
        image_size = 400
        image_x = (canvas_width - image_size) // 2
        image_y = (canvas_height - image_size) // 2

        azure_vision_endpoint = st.text_input('Azure Computer Vision Endpoint')  # added this line
        azure_vision = st.text_input('Azure Computer Vision API Key')  # added this line
        organization = st.text_input('OpenAI Organization')
        api_key = st.text_input('OpenAI API Key')
        openai.api_key=api_key
        openai.organization=organization

        # Define a list of image URLs
        image_urls = [
            "https://retailcontosoclothing.blob.core.windows.net/data4/GettyImages-157692462.jpg",
            "https://retailcontosoclothing.blob.core.windows.net/data4/GettyImages-1336682514.jpg"
            # Add more image URLs here if needed
        ]

        # Create a tab bar with images
        tabs = st.image(image_urls, width=150)

        # Wait for the user to select a tab
        selected_tab = st.radio("Select an image:", image_urls)
        if selected_tab == "https://retailcontosoclothing.blob.core.windows.net/data4/GettyImages-157692462.jpg":
            cloth_width = 850
            x,y =65,175
            default_width=400
            default_x=290
            default_y=10
        elif selected_tab == "https://retailcontosoclothing.blob.core.windows.net/data4/GettyImages-1336682514.jpg":
            cloth_width = 650
            x,y =150,250
            default_width=300
            default_x=340
            default_y=30
        # Load the selected image and display it on the canvas
        response = requests.get(selected_tab)
        cloth_image = Image.open(BytesIO(response.content))
        uploaded_front = st.file_uploader("Upload the front image...", type=["jpg", "jpeg", "png"])
        uploaded_back = st.text_input("Enter text:", value= "a room, Domestic interiors")

        if "front_image2" not in st.session_state or "cloth_image" not in st.session_state:
            st.session_state.front_image2 = None
            st.session_state.cloth_image = None

        if uploaded_front is not None and uploaded_back is not None:
            # Load the images and display them on the canvas
            front = Image.open(io.BytesIO(uploaded_front.read()))
            face = face_crop(front,azure_vision,azure_vision_endpoint)
            removal = background_removal(face,azure_vision,azure_vision_endpoint)
            removal_U=  U_crop(removal)
            cloth_removal= background_removal(cloth_image,azure_vision,azure_vision_endpoint)
            front_image = Image.open(BytesIO(removal_U))
            cloth_image = Image.open(BytesIO(cloth_removal))

            st.session_state.front_image2 = front_image
            st.session_state.cloth_image = cloth_image
            # Calculate the aspect ratio of the front image
            aspect_ratio = st.session_state.front_image2.size[1] / st.session_state.front_image2.size[0]
            aspect_ratio_c = st.session_state.cloth_image.size[1] / st.session_state.cloth_image.size[0]
            # Allow the user to set the width, horizontal position, and vertical position of the front image
            with st.sidebar:
                front_width = st.slider("Set the width of the front image:", min_value=50, max_value=2000, value=default_width, step=10)
                new_x_front = st.slider("Move the front image horizontally:", min_value=0, max_value=canvas_width, value=default_x, step=10)
                new_y_front = st.slider("Move the front image vertically:", min_value=0, max_value=canvas_height, value=default_y, step=10)
                x = st.slider("Move the cloth image horizontally:", min_value=0, max_value=canvas_width, value=x, step=10)
                y = st.slider("Move the cloth image vertically:", min_value=0, max_value=canvas_height, value=y, step=10)
            # Calculate the height of the front image based on the aspect ratio and the desired width
            front_height = int(front_width * aspect_ratio)

            # front_height = display_images(st.session_state.front_image2, front_width)

            cloth_height = int(cloth_width*aspect_ratio_c)
            canvas_image, new_front = move_images3(st.session_state.front_image2, front_width, front_height, new_x_front, new_y_front, st.session_state.cloth_image,cloth_width,cloth_height,x,y,canvas_width, canvas_height)

            if st.button("Generate Image"):
                new_image = dalle_edit(new_front, uploaded_back)

                # Display the canvas_image using streamlit
                st.image(new_image, use_column_width=False, width=canvas_width)

                # Convert the image url to a PIL image
                response = requests.get(new_image)
                image = Image.open(BytesIO(response.content))
                
                # Save the image as a PNG file
                with BytesIO() as output:
                    image.save(output, format="PNG")
                    png_data = output.getvalue()
                print(len(png_data))   
                # Download the PNG file
                b64 = base64.b64encode(png_data).decode()
                href = f'<a href="data:file/png;base64,{b64}" download="image.png" style="font-size: 20px;">Download PNG file</a>'

                
                st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    # Add CSS to center the content and canvas
    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container {{
                max-width: 1200px;
                padding-top: 1rem;
                padding-right: 1rem;
                padding-left: 1rem;
                padding-bottom: 1rem;
            }}
            .reportview-container .main {{
                align-items: center;
            }}
            .stApp {{
                margin: 0 auto;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    main()

