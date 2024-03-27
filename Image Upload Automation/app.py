import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageOps
import os
import datetime
import requests

def resize_image(uploaded_file, aspect_ratio):
    original_image = Image.open(uploaded_file)
    
    # Convert to OpenCV format for processing
    opencv_image = np.array(original_image)
    
    # Convert to grayscale for edge detection
    gray_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2GRAY)
    
    # Apply edge detection (adjust parameters as needed)
    edges = cv2.Canny(gray_image, 50, 150)
    
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get the largest contour (assumed to be the subject)
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Get the bounding box around the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Crop the original image to the bounding box
    cropped_image = original_image.crop((x, y, x + w, y + h))

    # Calculate new height while maintaining the aspect ratio
    new_height = int(cropped_image.width / aspect_ratio)

    # Resize the cropped image
    resized_image = cropped_image.resize((cropped_image.width, new_height))
    
    return resized_image

def upload_to_website(image_path, website_url):
    try:
        # Open the image file in binary mode
        with open(image_path, 'rb') as image_file:
            # Prepare the files dictionary with the key as 'file'
            files = {'file': (image_path, image_file, 'image/jpeg')}
            
            # Make a POST request to the website's upload endpoint
            response = requests.post(website_url, files=files)
            
            # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                print("Image uploaded successfully!")
            else:
                print(f"Failed to upload image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error uploading image: {e}")

def main():
    st.title("Image Processing and Upload App")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Resize image to a fixed aspect ratio
        aspect_ratio = 16 / 9  # Adjust this according to your requirements
        resized_image = resize_image(uploaded_file, aspect_ratio)

        # Center the image around the subject
        subject_coordinates = (resized_image.width / 2, resized_image.height / 2)
        centered_image = center_image(resized_image, subject_coordinates)

        # Save the processed image
        save_path = f"processed_images/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        centered_image.save(save_path)

        # Upload the image to the live website
        website_url = "https://your-website.com/upload"  # Replace with your actual website URL
        upload_to_website(save_path, website_url)

        # Display the processed image
        st.image(centered_image, caption="Processed Image", use_column_width=True)

if __name__ == "__main__":
    main()