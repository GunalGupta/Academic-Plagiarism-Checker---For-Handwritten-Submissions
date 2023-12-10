from scipy.spatial.distance import cosine
from skimage import io, color, feature
from udp import generate_digital_pattern, compare_patterns
from ocr import extract_text, compare_text_content
import os
from sentence_transformers import SentenceTransformer,util
from openai_model import compare_text_similarity

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
    cp_list = []
    pp_list = []

    for i in range(len(submissions)):
        # Checking if particular submission is already under Complete Plagiarism
        if submissions[i] in excluded_docs: continue
        for j in range(i + 1, len(submissions)):
            
            pattern1 = pattern_list[i]
            pattern2 = pattern_list[j]

            # Ensuring that patterns have the same length
            min_len = min(len(pattern1), len(pattern2))
            pattern1 = pattern1[:min_len]
            pattern2 = pattern2[:min_len]
            file1 = submissions[i]
            file2 = submissions[j]

            # Extract the filename without extension from file1
            filename1, extension1 = os.path.splitext(file1)
            file1 = filename1

            # Extract the filename without extension from file2
            filename2, extension2 = os.path.splitext(file2)
            file2 = filename2  

            similarity = compare_patterns(pattern1, pattern2)
            if similarity > 0.95:
                print(f"\nLevel 1: Complete Plagiarism detected between {file1} and {file2}")
                excluded_docs[submissions[j]] = True
                cp_list.append((file1, file2))

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
                        print(f"\nLevel 2: Complete Plagiarism detected between {file1} and {file2}")
                        excluded_docs[submissions[j]] = True
                        cp_list.append((file1, file2))
                    else:
                        print(f"\nLevel 2: Potential Plagiarism detected between {file1} and {file2} with a UDP score = {similarity*100:.2f}% and Content Similarity score = {similarity_score*100:.2f}% ")
                        # level2_list.append((file1, file2))
                        pp_list.append((file1, file2))
                else:
                    print(f"\nLevel 2: Potential Plagiarism detected between {file1} and {file2} with a UDP score = {similarity*100:.2f}%")
                    # level2_list.append((file1, file2))
                    pp_list.append((file1, file2))
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
                        print(f"\nLevel 3: Complete Plagiarism detected between {file1} and {file2}")
                        # level3_list.append((file1, file2))
                        cp_list.append((file1, file2))
                    elif cos_sim >= 0.75:
                        print(f"\nLevel 3: Potential Plagiarism detected between {file1} and {file2} with a similarity score = {similarity_score*100:.2f}%")
                        # level3_list.append((file1, file2))
                        pp_list.append((file1, file2))
                    # else:
                    #     print(f"\nLevel 3: No Plagiarism detected between {file1} and {file2} with a similarity score = {similarity_score*100:.2f}%")
                else:
                    print(f"\nUnable to load extracted text for {file1} and {file2}")
    # Level 4 - Testing for Paraphrasing
    level4_list = []
    value = int(input("\nDo you want to check for paraphrased ? (Alpha Phase) Enter 0 or 1: "))
    if value:
        for i in range(len(submissions)):
            if submissions[i] in excluded_docs: continue
            for j in range(i + 1, len(submissions)):
                text1 = text_list[i]
                text2 = text_list[j]
                if text1 and text2:
                    paraphrased = compare_text_similarity(text1, text2)
                    paraphrased = extract_similarity_value(paraphrased)
                    if paraphrased:
                        print(f"\nLevel 4: Potential Plagiarism detected between {file1} and {file2}")
                        level4_list.append((submissions[i], submissions[j]))
                else:
                    print(f"\nUnable to load extracted text for {file1} and {file2}")
    else:
        print("\nThank you for using our model. Have a nice day!")

    # Final Result Printing
    print("\n\n\n")
    print(f"Complete Plagiarism Pairs:- {cp_list}")
    print(f"\nPotential Plagiarism:- {pp_list}")
    print(f"\nParaphrased Plagiarism pairs - {level4_list}")
    print("\n\n\n")

# Location of Submission Folder
submission_folder = "submission_folder" #Relative Path address of your Submission Folder
scan_for_plagiarism(submission_folder)
