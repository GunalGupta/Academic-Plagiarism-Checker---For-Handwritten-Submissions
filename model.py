import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial.distance import cosine
from skimage import io, color, feature
from udp import generate_digital_pattern, compare_patterns
from ocr import extract_text, compare_text_content
import os
import requests


# Function to scan and compare all submissions
def scan_for_plagiarism(submission_folder):
    submissions = os.listdir(submission_folder)
    
    text_list = []
    pattern_list = []

    # Temporary storing UDPs and extracting text of every submission file
    for i in range(len(submissions)):
        # Generating digital pattern for submission file
        pattern = generate_digital_pattern(os.path.join(submission_folder, submissions[i]))

        # Store Pattern in List
        pattern_list.append(pattern)

        # Extracting Text
        text = extract_text(os.path.join(submission_folder, submissions[i]))

        # Store text in the list
        text_list.append(text)

    excluded_docs = {}

    for i in range(len(submissions)):
        if submissions[i] in excluded_docs: continue
        for j in range(i + 1, len(submissions)):

            pattern1 = pattern_list[i]
            pattern2 = pattern_list[j]

            # Ensuring that patterns have the same length
            min_len = min(len(pattern1), len(pattern2))
            pattern1 = pattern1[:min_len]
            pattern2 = pattern2[:min_len]

            similarity = compare_patterns(pattern1, pattern2)
            if similarity > 0.95:
                print(f"Complete Plagiarism detected between {submissions[i]} and {submissions[j]}")
                excluded_docs[submissions[j]] = True

            # Adjust the threshold based on requirements
            elif similarity > 0.50:
                print(f"Potential Plagiarism detected between {submissions[i]} and {submissions[j]} with a similarity score = {similarity*100:.2f}%")
            else:
                # Extracting text from the suspicious submissions
                text1 = text_list[i]
                text2 = text_list[j]

                # Compare extracted text
                if text1 and text2:
                    if compare_text_content(text1, text2):
                        print(f"Same text content detected between {submissions[i]} and {submissions[j]}")
                        excluded_docs[submissions[j]] = True
                     # else: 
                    #     print("Different text content detected.")
                    #     print(f"{text1}")
                    #     print(f"\n\n{text2}")
                else:
                    print(f"Error while comparing text between {submissions[i]} and {submissions[j]}")

# Location of Submission Folder
submission_folder = "submission_folder" #Relative Path address of your Submission Folder
scan_for_plagiarism(submission_folder)
