import pytesseract
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial.distance import cosine
from skimage import io, color, feature
import os
import requests

# Function to extract text from an image using Tesseract OCR
def extract_text(image_path):
    try:
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(io.imread(image_path))
        return text
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}")
        return ""

# Function to compare extracted text content
def compare_text_content(text1, text2):
    return text1.lower() == text2.lower()
