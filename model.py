import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial.distance import cosine
from skimage import io, color, feature
from ocr import extract_text
import os
import io

# Function to generate a digital pattern from a handwritten image
def generate_digital_pattern(image_path):
    # Load the image
    image = io.imread(image_path)

    # Check if the image is not already a numpy array
    if not isinstance(image, np.ndarray):
        # Convert the image to RGB
        image = image.convert('RGB')

    # Convert the RGB image to a numpy array
    image_array = np.array(image)

    # Calculate the grayscale values for each pixel
    grayscale_array = 0.2125 * image_array[:, :, 0] + 0.7154 * image_array[:, :, 1] + 0.0721 * image_array[:, :, 2]

    # Convert the grayscale array back to an image
    grayscale_image = Image.fromarray(grayscale_array.astype(np.uint8))

    # Extract features using Histogram of Oriented Gradients (HOG)
    features = feature.hog(grayscale_image, pixels_per_cell=(16, 16))

    return features

# Function to compare digital patterns using cosine similarity
def compare_patterns(pattern1, pattern2):
    # Use cosine similarity as the comparison metric
    similarity = 1 - cosine(pattern1, pattern2)
    return similarity


# Function to scan and compare all submissions
def scan_for_plagiarism(submission_folder):
    submissions = os.listdir(submission_folder)

    for i in range(len(submissions)):
        for j in range(i + 1, len(submissions)):
            pattern1 = generate_digital_pattern(os.path.join(submission_folder, submissions[i]))
            pattern2 = generate_digital_pattern(os.path.join(submission_folder, submissions[j]))

            # Ensure that patterns have the same length
            min_len = min(len(pattern1), len(pattern2))
            pattern1 = pattern1[:min_len]
            pattern2 = pattern2[:min_len]

            similarity = compare_patterns(pattern1, pattern2)

            # Adjust the threshold based on your requirements
            if similarity > 0.55:
                print(f"Potential plagiarism detected between {submissions[i]} and {submissions[j]} with a similarity score = {similarity*100:.2f}%")

                # Extract text from the suspicious submissions
                text1 = extract_text(os.path.join(submission_folder, submissions[i]))
                text2 = extract_text(os.path.join(submission_folder, submissions[j]))

                # Compare extracted text
                if text1 and text2:
                    if text1.lower() == text2.lower():
                        print("Same text content detected.")
                    else:
                        print("Different text content detected.")
                        print(f"{text1}")
                        print(f"\n\n{text2}")
                else:
                    print("Error extracting text for comparison.")

# Location of Submission Folder
submission_folder = "submission_folder" #Relative Path address of your Submission Folder
scan_for_plagiarism(submission_folder)
