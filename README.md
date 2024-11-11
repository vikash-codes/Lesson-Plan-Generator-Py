# Lesson Plan Generator

## Overview
The Lesson Plan Generator is a web application designed to help educators create structured and visually appealing lesson plans from PDF textbook chapters. The app allows users to upload PDFs, extracts key concepts, and generates customizable lesson plans, which can be saved, edited, and downloaded.

## Technologies Used
- **Backend**: Flask
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Database and Authentication**: Firebase Firestore and Firebase Authentication
- **APIs**: Unsplash API for images, spaCy for NLP-based keyword extraction
- **Other**: Gunicorn for production

## Installation Instructions
1. **Clone the repository**:
   ```bash
   git clone https://github.com/vikash-codes/Lesson-Plan-Generator-Py.git
   cd your-repo-name
## Setup virtual environment ##
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
## install dependencies ##
    pip install -r requirements.txt
## Run the code ##
    python app.py
    ```