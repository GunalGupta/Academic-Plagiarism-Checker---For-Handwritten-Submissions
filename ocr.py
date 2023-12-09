import pytesseract
import os
import io

# Function to extract text from an image using Tesseract OCR
def extract_text(image_path):
    try:
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(io.imread(image_path))
        return text
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}")
        return ""
