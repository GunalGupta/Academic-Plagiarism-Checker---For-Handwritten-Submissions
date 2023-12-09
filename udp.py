import numpy as np
from PIL import Image
from scipy.spatial.distance import cosine
from skimage import io, color, feature
import os

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