import streamlit as st
import os
import zipfile
from model import scan_for_plagiarism
import shutil  # Import the shutil module for file operations

st.set_page_config(
    page_title="Academic Plagiarism Detector🤖", layout="centered", initial_sidebar_state="auto"
)

def main():
    st.title("Academic Plagiarism Detector 🤖")
    with st.expander("Project Contributors"):
        st.write("Anubhav Dubey")
        st.write("Apurva Bajaj")
        st.write("Govind Garg")
        st.write("Gunal Gupta")
        st.write("Ved Vekhande")    
    # Upload zip file
    # st.header("Upload Zip File")
    uploaded_file = st.file_uploader("Choose a ZIP file", type="zip")
    checkbok = st.checkbox("Use Level 4 (OpenAI based Paraphrasing Detection) (Alpha Mode)")

    # Define the extraction destination as the directory of the current Python script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    print(script_directory)
    extraction_dest = os.path.join(script_directory)

    if uploaded_file is not None:
        if not zipfile.is_zipfile(uploaded_file):
            st.error("Uploaded file is not a valid ZIP file. Please choose a ZIP file.")
        else:
            folder_name, _ = os.path.splitext(uploaded_file.name)
            destination_folder = os.path.join(extraction_dest, folder_name)
            # Check whether the folder uploaded already exist in the directory, if not then extract it, else use the already extracted folder
            # Done only to save space on the VM hosted, rather you can just comment out this condition
            if not os.path.exists(destination_folder):

                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    # Create the destination directory if it doesn't exist
                    os.makedirs(extraction_dest, exist_ok=True)

                    # Extract files directly to the specified directory
                    zip_ref.extractall(extraction_dest)
                    # st.write("Files extracted.")
                    
                    # Run plagiarism detection when the user clicks the button
                    if st.button("Detect Plagiarism"):
                        print("Used New folder")
                        file_name, file_extension = os.path.splitext(uploaded_file.name)

                        print(file_name)
                        # Run plagiarism detection on the extracted folder
                        scan_for_plagiarism(file_name, checkbok)

            else:
                if st.button("Detect Plagiarism"):
                    print("Used previous folder")
                    file_name, file_extension = os.path.splitext(uploaded_file.name)
                    print(file_name)
                    # Run plagiarism detection on the extracted folder
                    scan_for_plagiarism(file_name, checkbok)

if __name__ == "__main__":
    main()