import cv2
import numpy as np
from sklearn import svm
from scipy.spatial import distance

# Step 1: Load the images
image_A = cv2.imread('ImageA.jpg', cv2.IMREAD_GRAYSCALE)
image_B = cv2.imread('ImageB.jpg', cv2.IMREAD_GRAYSCALE)
image_C = cv2.imread('ImageC.jpg', cv2.IMREAD_GRAYSCALE)
image_D = cv2.imread('ImageD.jpg', cv2.IMREAD_GRAYSCALE)
image_E = cv2.imread('ImageE.jpg', cv2.IMREAD_GRAYSCALE)

# Step 2: Preprocess the images
def preprocess_image(image):
    # Apply Gaussian blur
    image = cv2.GaussianBlur(image, (5, 5), 0)
    
    # Binarize the image
    _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Resize the image to a standard size
    image = cv2.resize(image, (32, 32))
    
    # Flatten the image
    image = image.flatten()
    
    return image

# Preprocess all images
images = [image_A, image_B, image_C, image_D, image_E]
preprocessed_images = [preprocess_image(image) for image in images]

# Step 3: Train a SVM model on the preprocessed images
labels = [0, 1, 2, 3, 4]
model = svm.SVC(gamma=0.001, C=100.)
model.fit(preprocessed_images, labels)

# Step 4: Generate a unique digital pattern (UDP) for each image
udps = model.predict(preprocessed_images)

# Step 5: Compare the UDPs to detect potential plagiarism
for i in range(len(udps)):
    for j in range(i + 1, len(udps)):
        # Flatten the UDPs into 1-D arrays
        udp_i = np.array(udps[i]).flatten()
        udp_j = np.array(udps[j]).flatten()
        if udps[i] == udps[j]:
            print(f"Image {i} and Image {j} might be plagiarized.")