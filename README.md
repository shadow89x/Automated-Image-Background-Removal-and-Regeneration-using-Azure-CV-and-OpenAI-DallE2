# Image Processing Application

## Table of Contents

- [Overview](#overview)
- [Instructions for Use](#instructions-for-use)
- [Code Structure](#code-structure)
- [Example Usage](#example-usage)
- [API References](#api-references)
- [Dependencies](#dependencies)
- [Contributions](#contributions)
- [License](#license)

## Overview

This Python-based web application allows users to manipulate and process images using different techniques. The application leverages the powerful Streamlit framework for the interactive front-end, and integrates OpenAI and Azure AI for image generation and processing. 

Main features include:
- Background Removal
- Face Cropping
- Image Masking 
- Image Generation using OpenAI 
- Image manipulation including moving, scaling and saving images

## Instructions for Use

1. Clone or download the repository to your local machine.
2. Install the required dependencies listed in `requirements.txt`. You can use `pip install -r requirements.txt` to install them.
3. Obtain the necessary API keys for Azure Vision and OpenAI.
4. Run `streamlit run app.py` from your command line.
5. Access the app by navigating to the URL displayed in your terminal (usually `http://localhost:8501`).

## Working with the Application

Before diving into the workings of the application, ensure that you've set up your environment correctly. You will need API keys from OpenAI and Azure Computer Vision. If you don't have organization key, leave the corresponding variable in the code blank.

### 1. Background Replacement using OpenAI DallE2 and Azure Computer Vision

The first feature of this application allows you to replace the background of an image using OpenAI's DallE2 and Azure's Computer Vision. Here's how it works:

1. Upload a photo.
2. Azure Computer Vision removes the background of your image.
3. OpenAI's DallE2 generates an image from your prompt and replaces the background with this image.

<img src="https://live.staticflickr.com/65535/53006832402_a79ca2bfd2_z.jpg" width="500">

After the images are generated, you can move and resize the result using the slider in the sidebar.

<img src="https://live.staticflickr.com/65535/53007424136_54713a8ed4_z.jpg" width="500">

### 2. Background Replacement using OpenAI DallE2 Edit and Azure Computer Vision

The second feature is another method of changing the background. This time, we'll use OpenAI's DallE2 edit feature.

1. Remove the background with Azure's Computer Vision.
2. 'Extend' the missing image parts using the DallE2 edit feature by providing a prompt.

<img src="https://live.staticflickr.com/65535/53007590829_4c86fdeef4_z.jpg" width="500">

You'll need to resize and move the previously generated DallE2 edit image (since the edit feature fills the image based on the prompt). For optimal results, use a sufficiently large front image. If the front image is too small compared to the canvas size, the outcome might not be satisfactory.

<img src="https://live.staticflickr.com/65535/53007590819_3d64590929_z.jpg" width="500">

Below is an example of the result:

<img src="https://live.staticflickr.com/65535/53007908343_26bcf17a7c_z.jpg" width="500">

### 3. Virtual Try-On with Online Shopping

Ever wished you could try on clothes while shopping online? This application feature makes that possible. 

1. Upload a photo of your face. Azure Computer Vision will recognize your facial coordinates and crop the image.
2. By using OpenAI's edit feature, you can virtually try on the clothing of your choice.

First, select your clothing and provide a prompt for the background:

<img src="https://live.staticflickr.com/65535/53007590834_b13830bbd0_c.jpg" width="500">

Then, upload your photo:

<img src="https://upload.wikimedia.org/wikipedia/commons/3/34/Elon_Musk_Royal_Society_%28crop2%29.jpg" width="500">

Here's an example result:

<img src="https://live.staticflickr.com/65535/53007424161_af45a274a1_z.jpg" width="500">

## Code Structure

The application is primarily structured in two Python files: 

- `app.py`: This is the main application file where the Streamlit user interface is defined. This file is responsible for managing the front-end elements and interactions.
- `function.py`: This file contains all the functions used for image processing, including background removal, face cropping, image generation, etc. The functions here communicate with Azure Vision and OpenAI APIs.

## Example Usage

When you run the application, you will be able to upload your images for processing. 

- For background removal and face cropping, upload your image, and the processed image will be displayed. 
- For image generation, input your text prompt and the application will generate an image accordingly. 
- For image manipulation, you can move and scale the images, and also save the resulting image. 

## API References

- [Azure Vision](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/home): For image analysis and processing
- [OpenAI](https://beta.openai.com/docs/): For generating images from textual prompts

## Dependencies

This application relies on several Python libraries, including:

- [Streamlit](https://streamlit.io/): For building the web app and interactive UI
- [Pillow (PIL)](https://pillow.readthedocs.io/en/stable/): For image manipulation
- [OpenAI](https://beta.openai.com/docs/): For communicating with OpenAI API
- [Azure AI](https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-overview): For using Azure's Vision API
- [Requests](https://docs.python-requests.org/en/latest/), [IO](https://docs.python.org/3/library/io.html), [JSON](https://docs.python.org/3/library/json.html), [base64](https://docs.python.org/3/library/base64.html): For handling HTTP requests and data manipulation
- [Matplotlib](https://matplotlib.org/): For some auxiliary visualizations (optional)

## Contributions

This project is open for improvements and maintenance. Feel free to contribute and enhance the functionality of this image processing application.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

