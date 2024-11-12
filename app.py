from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
import os
import fitz  # PyMuPDF
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
import requests

import spacy
nlp = spacy.load("en_core_web_sm")

UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")

app = Flask(__name__)

# Directly assign the Unsplash API key since it's hard-coded here
UNSPLASH_API_KEY = "dAeY_8kgeJ8Dww9_H201Us6vKYYVVqXN5uHiFhNKips"

def fetch_illustration(keyword):
    url = f"https://api.unsplash.com/photos/random?query={keyword}&client_id={UNSPLASH_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['urls']['regular']  # Return the regular-sized image URL
    else:
        print("Error fetching illustration:", response.json())  # Print any error message from the API
    return None

# app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'your_secret_key'  # Needed for flash messages

generated_lesson_plan = None  # Initialize globally

def extract_keywords(text, num_keywords=10):
    doc = nlp(text)
    keywords = []

    # Extract named entities and nouns as keywords
    for entity in doc.ents:
        if entity.label_ in ["PERSON", "ORG", "GPE", "PRODUCT", "EVENT"]:
            keywords.append(entity.text)
    
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and token.is_alpha:
            keywords.append(token.text)

    # Return unique keywords and limit to specified count
    return list(set(keywords))[:num_keywords]

def generate_lesson_plan(keywords):
    introduction = f"This lesson covers the fundamental concepts related to {', '.join(keywords[:3])}. Students will gain an understanding of these topics."
    main_body = f"In the main content, we will explore {keywords[0]}, {keywords[1]}, and {keywords[2]} in depth. We’ll discuss how each concept is interconnected and its real-world applications."
    class_activity = f"For the class activity, students will be asked to research examples of {keywords[3]} and {keywords[4]}. They will work in groups to present their findings."
    return {
        "introduction": introduction,
        "main_body": main_body,
        "class_activity": class_activity
    }
   

def create_pdf(lesson_plan):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Lesson Plan")

    # Set up styles
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Generated Lesson Plan")
    
    # Introduction section
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, 720, "Introduction:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(100, 700, lesson_plan["introduction"])

    # Main Body section with bullet points
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, 670, "Main Body:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(100, 650, f"• {lesson_plan['main_body']}")

    # Class Activity section with bullet points
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, 620, "Class Activity:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(100, 600, f"• {lesson_plan['class_activity']}")

    # Finalize the page and save
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    global generated_lesson_plan
    # Check if a lesson plan has been generated
    if generated_lesson_plan is None:
        flash("Please upload a PDF and generate a lesson plan first.")
        return redirect(url_for('index'))
    return render_template('lesson_plan.html', lesson_plan=generated_lesson_plan)

@app.route('/saved_plans')
def saved_plans():
    return render_template('saved_plans.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        flash("No file part in the request.")
        return redirect(url_for('index'))

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        flash("No file selected. Please upload a PDF file.")
        return redirect(url_for('index'))

    if not pdf_file.filename.lower().endswith('.pdf'):
        flash("Invalid file type. Please upload a PDF file.")
        return redirect(url_for('index'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(file_path)

    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()

    keywords = extract_keywords(text)
    global generated_lesson_plan 
    generated_lesson_plan = generate_lesson_plan(keywords)

    illustration1 = fetch_illustration(keywords[0])
    illustration2 = fetch_illustration(keywords[1])

    return render_template('lesson_plan.html', lesson_plan=generated_lesson_plan, illustration1=illustration1, illustration2=illustration2)

@app.route('/download_saved_pdf')
def download_saved_pdf():
    plan_index = int(request.args.get("plan", 0))
    # Assuming `lesson_plans` holds saved plans. Replace with actual retrieval from Firestore if needed.
    user = firebase.auth().current_user
    user_id = user.uid
    plans = db.collection("users").document(user_id).collection("lessonPlans").get()
    selected_plan 

@app.route('/download_pdf')
def download_pdf():
    # Ensure there’s a generated lesson plan to download
    global generated_lesson_plan
    if generated_lesson_plan is None:
        flash("No lesson plan available for download.")
        return redirect(url_for('index'))
    buffer = create_pdf(generated_lesson_plan)
    return send_file(buffer, as_attachment=True, download_name="Lesson_Plan.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
