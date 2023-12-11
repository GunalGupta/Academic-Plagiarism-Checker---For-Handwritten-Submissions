from scipy.spatial.distance import cosine
from skimage import io, color, feature
from udp import generate_digital_pattern, compare_patterns
from ocr import extract_text, compare_text_content
import os
from sentence_transformers import SentenceTransformer,util
from openai_model import compare_text_similarity, extract_similarity_value 
import streamlit as st
model = SentenceTransformer('all-MiniLM-L6-v2')


# Function to scan and compare all submissions
def scan_for_plagiarism(submission_folder, checkbok):
    with st.spinner("Scanning for Plagiarism"):
        submissions = os.listdir(submission_folder)
        
        text_list = []

        for i in range(len(submissions)):
            # pattern = generate_digital_pattern(os.path.join(submission_folder, submissions[i]))
            text = extract_text(os.path.join(submission_folder, submissions[i]))

            # Store text in the list
            text_list.append(text)

        excluded_docs = {}
        cp_list = []
        pp_list = []
        level4_list = []
        with st.expander("Live Processing"):
            for i in range(len(submissions)):
                if submissions[i] in excluded_docs: continue
                for j in range(i + 1, len(submissions)):
                    
                    pattern1 = generate_digital_pattern(os.path.join(submission_folder, submissions[i]))
                    pattern2 = generate_digital_pattern(os.path.join(submission_folder, submissions[j]))

                    # Ensure that patterns have the same length
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
                        # print(f"\nLevel 1: Complete Plagiarism detected between {file1} and {file2}")
                        st.write(f"\nLevel 1: Complete Plagiarism detected between {file1} and {file2}")
                        excluded_docs[submissions[j]] = True
                        # level1_list.append((file1, file2))
                        cp_list.append((file1, file2))

                    # Adjust the threshold based on your requirements
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
                                st.write(f"\nLevel 2: Complete Plagiarism detected between {file1} and {file2}")
                                excluded_docs[submissions[j]] = True
                                # level2_list.append((file1, file2))
                                cp_list.append((file1, file2))
                            else:
                                st.write(f"\nLevel 2: Potential Plagiarism detected between {file1} and {file2} with a UDP score = {similarity*100:.2f}% and Content Similarity score = {similarity_score*100:.2f}% ")
                                # level2_list.append((file1, file2))
                                pp_list.append((file1, file2))
                        else:
                            st.write(f"\nLevel 2: Potential Plagiarism detected between {file1} and {file2} with a UDP score = {similarity*100:.2f}%")
                            # level2_list.append((file1, file2))
                            pp_list.append((file1, file2))
                    else:
                        # Extract text from the suspicious submissions
                        text1 = text_list[i]
                        text2 = text_list[j]

                        # Compare extracted text
                        if text1 and text2:
                            emb1 = model.encode(text1)
                            emb2 = model.encode(text2)
                            cos_sim = util.cos_sim(emb1, emb2)
                            similarity_score = cos_sim.item()
                            if cos_sim >= 0.85:
                                st.write(f"\nLevel 3: Complete Plagiarism detected between {file1} and {file2}")
                                # level3_list.append((file1, file2))
                                cp_list.append((file1, file2))
                            elif cos_sim >= 0.75:
                                st.write(f"\nLevel 3: Potential Plagiarism detected between {file1} and {file2} with a similarity score = {similarity_score*100:.2f}%")
                                # level3_list.append((file1, file2))
                                pp_list.append((file1, file2))
                        else:
                            st.write(f"\nUnable to load extracted text for {file1} and {file2}")
            # Level 4 - Testing for Paraphrasing
            
            # value = int(input("\nDo you want to check for paraphrased ? (Alpha Phase) Enter 0 or 1: "))
            if checkbok:
                for i in range(len(submissions)):
                    if submissions[i] in excluded_docs: continue
                    for j in range(i + 1, len(submissions)):
                        text1 = text_list[i]
                        text2 = text_list[j]
                        if text1 and text2:
                            paraphrased = compare_text_similarity(text1, text2)
                            paraphrased = extract_similarity_value(paraphrased) #extracting the integer value from the sentence, if openai returned sentencea as output instead of binary
                            if paraphrased:
                                st.write(f"\nLevel 4: Potential Plagiarism detected between {file1} and {file2}")
                                level4_list.append((submissions[i], submissions[j]))
                        else:
                            st.write(f"\nUnable to load extracted text for {file1} and {file2}")
                # print(f"Level 4: Paraphrased Plagirism pairs - {level4_list}")
            else:
                print("\nThank you for using our model. Have a nice day!")

            # Final Result Printing
        # print("\n\n\n\n\n")
        with st.expander("Complete Plagiarism Pairs"):
            st.write(f"Complete Plagiarism Pairs:- {cp_list}")
        with st.expander("Potential Plagiarism Pairs"):
            st.write(f"Potential Plagiarism:- {pp_list}")
        if checkbok:
            with st.expander("Paraphrased Plagirism pairs"):
                st.write(f"Paraphrased Plagirism pairs - {level4_list}")
