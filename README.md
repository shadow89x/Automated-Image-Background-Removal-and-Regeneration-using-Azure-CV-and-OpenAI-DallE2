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

