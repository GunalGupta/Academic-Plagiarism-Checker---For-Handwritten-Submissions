from scipy.spatial.distance import cosine
from skimage import io, color, feature
from udp import generate_digital_pattern, compare_patterns
from ocr import extract_text, compare_text_content
import os
from sentence_transformers import SentenceTransformer,util

model = SentenceTransformer('all-MiniLM-L6-v2')


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
            elif similarity > 0.55:
                text1 = text_list[i]
                text2 = text_list[j]

                # Compare extracted text
                if text1 and text2:
                    emb1 = model.encode(text1)
                    emb2 = model.encode(text2)
                    cos_sim = util.cos_sim(emb1, emb2)
                    similarity_score = cos_sim.item()
                    if cos_sim >= 0.85:
                        print(f"Complete Plagiarism detected between {submissions[i]} and {submissions[j]}")
                        excluded_docs[submissions[j]] = True
                    else:
                        print(f"Potential Plagiarism detected between {submissions[i]} and {submissions[j]} with a UDP score = {similarity*100:.2f}% and Content Similarity score = {similarity_score*100:.2f}% ")
                else:
                    print(f"Potential Plagiarism detected between {submissions[i]} and {submissions[j]} with a UDP score = {similarity*100:.2f}%")
            else:
                # Compare text from the suspicious submissions
                text1 = text_list[i]
                text2 = text_list[j]

                # Compare extracted text
                if text1 and text2:
                    emb1 = model.encode(text1)
                    emb2 = model.encode(text2)
                    cos_sim = util.cos_sim(emb1, emb2)
                    similarity_score = cos_sim.item()
                    if cos_sim >= 0.85:
                        print(f"Complete Plagiarism detected between {submissions[i]} and {submissions[j]}")
                    elif cos_sim >= 0.75:
                        print(f"\nPotential Plagiarism detected between {submissions[i]} and {submissions[j]} with a similarity score = {similarity_score*100:.2f}%")
                    # else
                    #     print(f"\nLevel 3: No Plagiarism detected between {file1} and {file2} with a similarity score = {similarity_score*100:.2f}%")
                else:
                    print(f"\nUnable to load extracted text for {submissions[i]} and {submissions[j]}")

# Location of Submission Folder
submission_folder = "submission_folder" #Relative Path address of your Submission Folder
scan_for_plagiarism(submission_folder)
