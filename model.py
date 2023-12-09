import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial.distance import cosine
from skimage import io, color, feature
from ocr import extract_text
from udp import generate_digital_pattern
from udp import compare_patterns
import os
import requests


# Function to scan and compare all submissions
def scan_for_plagiarism(submission_folder):
    submissions = os.listdir(submission_folder)

    for i in range(len(submissions)):
        for j in range(i + 1, len(submissions)):
            pattern1 = generate_digital_pattern(os.path.join(submission_folder, submissions[i]))
            pattern2 = generate_digital_pattern(os.path.join(submission_folder, submissions[j]))

            # Ensuring that patterns have the same length
            min_len = min(len(pattern1), len(pattern2))
            pattern1 = pattern1[:min_len]
            pattern2 = pattern2[:min_len]

            similarity = compare_patterns(pattern1, pattern2)

            # Adjust the threshold based on requirements
            if similarity > 0.55:
                print(f"Potential plagiarism detected between {submissions[i]} and {submissions[j]} with a similarity score = {similarity*100:.2f}%")

                # Extract text from the suspicious submissions
                text1 = extract_text(os.path.join(submission_folder, submissions[i]))
                text2 = extract_text(os.path.join(submission_folder, submissions[j]))

                # Compare extracted text
                if text1 and text2:
                    if text1.lower() == text2.lower():
                        print(f"Same text content detected between {submissions[i]} and {submissions[j]}")
                    else:
                        print(f"Different text content detected between {submissions[i]} and {submissions[j]}")
                        print(f"{text1}")
                        print(f"\n\n{text2}")
                else:
                    print(f"Error extracting text for comparison between {submissions[i]} and {submissions[j]}")

# Location of Submission Folder
submission_folder = "submission_folder" #Relative Path address of your Submission Folder
scan_for_plagiarism(submission_folder)
