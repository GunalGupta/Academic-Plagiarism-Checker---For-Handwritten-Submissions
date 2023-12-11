import os
import requests
from dotenv import load_dotenv
load_dotenv()
text_extract_api_key = os.getenv("text_extract_api_key")

# Function to extract text from an image using OCR
def extract_text(image_path):
    try:
        url = "https://api.apilayer.com/image_to_text/upload"

        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        headers= {
        "apikey": text_extract_api_key
        }

        response = requests.request("POST", url, headers=headers, data=image_data)

        status_code = response.status_code
        result = response.text
        # print("Result: ",result)
        return result
    
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}")
        return ""

# Function to compare extracted text content
def compare_text_content(text1, text2):
    return text1.lower() == text2.lower()
