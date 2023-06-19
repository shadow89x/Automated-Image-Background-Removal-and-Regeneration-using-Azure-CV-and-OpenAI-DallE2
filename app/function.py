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

openai.api_type = "open_ai"
openai.api_base = 'https://api.openai.com/v1'
openai.api_version = None




def background_removal(front_image,azure_vision,azure_vision_endpoint):
    url = f"{azure_vision_endpoint}/computervision/imageanalysis:segment?api-version=2023-02-01-preview&mode=backgroundRemoval"
    img_bytes = io.BytesIO()
    front_image.save(img_bytes, format='JPEG')
    binary_image = img_bytes.getvalue()


    headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': azure_vision
    }

    response = requests.request("POST", url, headers=headers, data=binary_image)

    return response.content

def face_crop(front_image,azure_vision,azure_vision_endpoint):
    url = f"{azure_vision_endpoint}//face/v1.0/detect"
    img_bytes = io.BytesIO()
    front_image.save(img_bytes, format='JPEG')
    binary_image = img_bytes.getvalue()

    payload = json.dumps({
    "url": "https://retailcontosoclothing.blob.core.windows.net/data/f178eeec-ad47-4a48-af2c-79683a4f1357.jpg?sp=r&st=2023-05-02T16:25:37Z&se=2023-06-01T00:25:37Z&spr=https&sv=2021-12-02&sr=b&sig=fxMuPxvlZO4hkkaCekn2LaEDc1PcDmL%2BNq7mBQ3gWgo%3D"
    })
    headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': azure_vision
    }

    response = requests.request("POST", url, headers=headers, data=binary_image)

    json_obj = json.loads(response.text)

    top=json_obj[0]['faceRectangle']['top']
    left=json_obj[0]['faceRectangle']['left']
    width=json_obj[0]['faceRectangle']['width']
    height=json_obj[0]['faceRectangle']['height']

    top=top*0.3
    if top < 0:
        top=0
    left=left*0.8
    width=width*2
    height=height*1.8

    # Define the bounding box coordinates
    box = (left, top, left + width, top + height)

    # Crop the image
    cropped_image = front_image.crop(box)

    return cropped_image



def U_crop(removal):
    # Retrieve the custom mask image from URL
    mask_url = "https://retailcontosoclothing.blob.core.windows.net/data4/U_mask.png"
    response = requests.get(mask_url)
    mask_image = Image.open(BytesIO(response.content)).convert("L")

    # Open the removal image as a PIL image
    removal_image = Image.open(BytesIO(removal))

    # Resize the mask image to match the size of the input image
    mask_image = mask_image.resize(removal_image.size, resample=Image.BILINEAR)

    # Apply the mask to the input image
    result = Image.new("RGBA", removal_image.size)
    result.paste(removal_image, mask=mask_image)

    # Convert the result image to bytes
    bytes_result = BytesIO()
    result.save(bytes_result, format='PNG')
    bytes_result.seek(0)

    return bytes_result.read()





def get_image(text):

    try:
        response = openai.Image.create(
        prompt=text,
        n=1,
        size="512x512"
        )
        image_url = response['data'][0]['url']
        return image_url
    except:
        print("Image Generation failed..")
        return None
    
@st.cache_data
def load_images1(uploaded_front, uploaded_back,azure_vision,azure_vision_endpoint):
    front = Image.open(io.BytesIO(uploaded_front.read()))

    removal = background_removal(front,azure_vision,azure_vision_endpoint)
    front_image = Image.open(BytesIO(removal))

    back_image_url = get_image(uploaded_back)
    print(back_image_url)

    back_image = Image.open(requests.get(back_image_url, stream=True).raw)

    return front_image, back_image

def display_images1(front_image, back_image, front_width, back_width):
    aspect_ratio = front_image.size[1] / front_image.size[0]
    front_height = int(front_width * aspect_ratio)

    st.sidebar.image(front_image.resize((200, round(200*aspect_ratio))), caption='Front Image', use_column_width=False)
    st.sidebar.image(back_image.resize((200, 200)), caption='Back Image', use_column_width=False)
    

    return front_height

def move_images1(front_image, back_image, front_width, back_width, front_height, new_x_front, new_y_front):
    resized_front = front_image.resize((front_width, front_height))
    resized_back = back_image.resize((back_width, back_width))
    canvas_image = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 255))
    canvas_image.paste(resized_back, (0, 0))
    canvas_image.paste(resized_front, (new_x_front, new_y_front), mask=resized_front)
    st.image(canvas_image, use_column_width=False, width=canvas_width)

    return canvas_image

@st.cache_data
def load_images(uploaded_front,azure_vision,azure_vision_endpoint):
    front = Image.open(io.BytesIO(uploaded_front.read()))

    removal = background_removal(front,azure_vision,azure_vision_endpoint)
    front_image = Image.open(BytesIO(removal))


    return front_image

def display_images(front_image, front_width):
    aspect_ratio = front_image.size[1] / front_image.size[0]
    front_height = int(front_width * aspect_ratio)

    st.sidebar.image(front_image.resize((200, round(200*aspect_ratio))), caption='Front Image', use_column_width=False)

    

    return front_height


def move_images(front_image, front_width, front_height, new_x_front, new_y_front,canvas_width, canvas_height):
    # Resize front_image
    resized_front = front_image.resize((front_width, front_height))
    
    # Create a new RGBA image for the canvas
    canvas_image = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 255))
    
    # Paste the resized front_image onto the canvas
    canvas_image.paste(resized_front, (new_x_front, new_y_front), mask=resized_front)
    
    
    # Draw a red square border around the front_image
    border_width = 10  # Change this value to adjust the border width
    draw = ImageDraw.Draw(canvas_image)
    draw.rectangle((0,0,1024,1024), outline="red", width=border_width)
    if (front_width or front_height) < 1024:
        if front_height<front_width:
            resize=front_width
        else:
            resize=front_height
    else:
        resize = 1024
    # Create a new transparent image of size 1024x1024
    new_image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    
    # Paste the resized_front onto the new image at the specified coordinates
    new_image.paste(resized_front, (new_x_front, new_y_front), mask=resized_front)
    
    # Save the new image as a temporary PNG variable
    temp_png = io.BytesIO()
    new_image.save(temp_png, format='PNG')
    
    # Display the canvas_image using streamlit
    st.image(canvas_image, use_column_width=False, width=canvas_width)
    
    return canvas_image,temp_png.getvalue()


def move_images3(front_image, front_width, front_height, new_x_front, new_y_front, cloth_image, x_cloth, y_cloth,x,y,canvas_width, canvas_height):
    # Resize front_image
    resized_front = front_image.resize((front_width, front_height))

    resized_cloth = cloth_image.resize((x_cloth, y_cloth))   
    # Create a new RGBA image for the canvas
    canvas_image = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 255))

    # Paste the resized front_image onto the canvas
    canvas_image.paste(resized_front, (new_x_front, new_y_front), mask=resized_front)

    # Paste the cloth_image onto the canvas
    canvas_image.paste(resized_cloth,(x,y), mask=resized_cloth)

    
    # Draw a red square border around the front_image
    border_width = 10  # Change this value to adjust the border width
    draw = ImageDraw.Draw(canvas_image)
    draw.rectangle((0, 0, 1024, 1024), outline="red", width=border_width)
    
    if (front_width or front_height) < 1024:
        if front_height < front_width:
            resize = front_width
        else:
            resize = front_height
    else:
        resize = 1024
    
    # Create a new transparent image of size 1024x1024
    new_image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    
    # Paste the resized_front onto the new image at the specified coordinates
    new_image.paste(resized_front, (new_x_front, new_y_front), mask=resized_front)
    

    # Paste the cloth_image onto the new image at the specified coordinates
    new_image.paste(resized_cloth,(x,y), mask=resized_cloth)
    


    # Save the new image as a temporary PNG variable
    temp_png = BytesIO()
    new_image.save(temp_png, format='PNG')
    
    # # Display the canvas_image using streamlit
    # st.image(canvas_image, use_column_width=False, width=canvas_width)
    
    return canvas_image, temp_png.getvalue()



def move_images2(front_image, back_image, front_width, back_width, front_height, new_x_front, new_y_front,canvas_width, canvas_height):
    resized_front = front_image.resize((front_width, front_height))
    resized_back = back_image.resize((back_width, back_width))
    canvas_image = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 255))
    canvas_image.paste(resized_back, (0, 0))
    canvas_image.paste(resized_front, (new_x_front, new_y_front), mask=resized_front)
    st.image(canvas_image, use_column_width=False, width=canvas_width)

    return canvas_image


def save_image(canvas_image):

    with io.BytesIO() as output:
        canvas_image.save(output, format="PNG")
        b64_string = base64.b64encode(output.getvalue()).decode()
        href = f'<a href="data:file/png;base64,{b64_string}" download="image.png" style="font-size: 20px;">Download PNG file</a>'

        st.markdown(href, unsafe_allow_html=True)


def dalle_edit(front_image,uploaded_back):
    # Upload the image to the OpenAI API
    response = openai.Image.create_edit(
    image=front_image,
    prompt=uploaded_back,
    n=1,
    size="1024x1024"
    )
    url=response['data'][0]['url']
    return url

def clear_session_state():
    st.session_state.front_image = None
    st.session_state.back_image = None
    st.session_state.front_image2 = None
    st.session_state.cloth_image = None
    st.session_state.clear()