# Academic Plagiarism Checker - For Handwritten Submissions 📝

This project aims to provide a solution for checking plagiarism in handwritten assignments submitted by students. The system combines digital pattern analysis and text content comparison between submission files to identify potential instances of plagiarism.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Background Model](#background-model)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Considering the advancements in interpersonal communication technologies today that bridge the most distant humans, it has never been easier to plagiarize 
handwritten assignments. A simple photograph of a person’s assignment can spread in seconds to the Deepest reaches of the globe. Online learning has exacerbated 
this practice to a great extent. Handwritten assignments shared among peers further undermine the prospects of acquiring the quality of learning that is achieved 
only when assignments are completed by the individual. It would be very simple to prevent plagiarism by accepting typed assignments and running a plagiarism check 
on them; however, many regions do not have access to computers, so accepting typed assignments in such situations would be impossible. Moreover, deciphering who 
copied from whom is a very time-consuming and difficult task for teachers. This is a situation which can be remedied by deploying a set of robust plagiarism detection 
algorithms in a model. The system uses a combination of digital pattern analysis through generating the UDP (Unique Digital Pattern) and text content comparison for 
each pair of submission to provide a comprehensive approach to plagiarism detection.

## Features

- **Digital Pattern Analysis:** Generates digital patterns from handwritten images using Histogram of Oriented Gradients (HOG).
- **Text Content Comparison:** Utilizes Optical Character Recognition (OCR) to extract text from images and compares the content for similarity.
- **Multi-level Detection:** Implements a multi-level detection approach to identify complete plagiarism and potential plagiarism with varying similarity scores.

## Requirements

- Python (>=3.6)
- Required Python Packages:
  - `numpy`
  - `PIL`
  - `scipy`
  - `scikit-image`
  - `os`
  - `requests`
  - `sentence-transformers`
  - `openai`

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/GunalGupta/Academic-Plagiarism-Checker---For-Handwritten-Submissions.git
    ```

2. Install the required packages:

    ```
    pip install -r requirements.txt
    ```

3. Replace `{Your API Key}` in the code with your actual API key for OCR functionality.

4. Replace `{Your API Key}` in the code with your actual API key for Open AI functionality.

## Usage

```
python model.py
```

## Methodology
<img width="550" alt="Methodology" src="https://github.com/GunalGupta/Academic-Plagiarism-Checker---For-Handwritten-Submissions/assets/97979413/eeaa80ac-fcf9-4123-bc45-f9416016042c">

## Background Model
<img width="550" alt="Model" src="https://github.com/GunalGupta/Academic-Plagiarism-Checker---For-Handwritten-Submissions/assets/97979413/4770e0f8-59e2-4c4d-be78-6fa502f10716">

## Results

The output will include filenames of the detected plagiarism pairs, helping you identify instances of complete and potential academic misconduct in the submissions.

## Contributing

This project was developed as part of an academic Design Project, and contributions specific to the project's goals are appreciated. While external contributions may 
not align with the project's immediate scope, feedback and suggestions for improvement are welcome.

### How to Provide Feedback

If you have feedback, suggestions, or ideas for improvement, please feel free to open an issue. While external code contributions might not be part of the immediate 
evaluation criteria, constructive feedback that enhances the project's design, functionality, or documentation is highly valued.

### Steps for Providing Feedback

1. **Open an Issue:** Clearly describe the feedback or suggestion in a new issue. Include details about the specific area or aspect you are addressing.

2. **Discussion:** Engage in discussions on the opened issue to further elaborate on the feedback or suggestion. This collaborative approach ensures a better
understanding of the proposed changes.

3. **Documentation:** If the feedback relates to documentation improvements, please specify the section or details that need clarification or enhancement.

Remember, your input contributes to the continuous improvement of the project, and thoughtful feedback is essential for its success.

## Contributors
*1. [Gunal Gupta](https://github.com/GunalGupta)* <br>
*2. [Ved Vekhande](https://github.com/ved-01)* <br>
*3. [Anubhav Dubey](https://github.com/AnubhavDubey23)* <br>
*4. [Govind Garg](https://github.com/itsggarg)*<br>
*5. [Apurva Bajaj](https://github.com/Bajaj-Apurva)*<br>

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code as per the terms of the license.


