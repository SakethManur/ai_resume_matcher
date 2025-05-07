# app.py

import os
import pdfplumber
import spacy
import re
from flask import Flask, render_template, request, redirect, url_for

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load Spacy model
nlp = spacy.load('en_core_web_sm')

# --------- Helper Functions --------- #
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]
    return tokens

def extract_skills(tokens, skill_set):
    extracted_skills = set()
    for token in tokens:
        if token in skill_set:
            extracted_skills.add(token)
    return list(extracted_skills)

def extract_experience(text):
    match = re.search(r'(\d+)\s+years', text.lower())
    if match:
        return int(match.group(1))
    return 0

def extract_education(text):
    education_keywords = ['bachelor', 'master', 'b.tech', 'm.tech', 'phd', 'degree']
    for word in education_keywords:
        if word in text.lower():
            return word
    return None

def calculate_match(resume_data, jd_data):
    required_skills = set(jd_data['skills'])
    resume_skills = set(resume_data['skills'])
    skill_match_percentage = (len(resume_skills & required_skills) / len(required_skills)) * 100 if required_skills else 0

    required_experience = jd_data['experience']
    resume_experience = resume_data['experience']
    experience_match_percentage = min((resume_experience / required_experience) * 100, 100) if required_experience else 0

    required_education = jd_data['education']
    resume_education = resume_data['education']
    education_match_percentage = 100 if resume_education and required_education and (required_education in resume_education) else 0

    final_score = (skill_match_percentage * 0.5) + (experience_match_percentage * 0.3) + (education_match_percentage * 0.2)
    return final_score, skill_match_percentage, experience_match_percentage, education_match_percentage

# --------- Flask Routes --------- #
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume = request.files['resume']
        jd = request.files['jd']

        if resume and jd:
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
            jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd.filename)
            resume.save(resume_path)
            jd.save(jd_path)

            resume_text = extract_text_from_pdf(resume_path)
            with open(jd_path, 'r', encoding='utf-8') as f:
                jd_text = f.read()

            skill_set = {"python", "java", "sql", "machine learning", "data analysis", "aws", "docker", "react", "c++", "cloud,","HTML","CSS",}

            resume_tokens = preprocess(resume_text)
            jd_tokens = preprocess(jd_text)

            resume_data = {
                'skills': extract_skills(resume_tokens, skill_set),
                'experience': extract_experience(resume_text),
                'education': extract_education(resume_text)
            }

            jd_data = {
                'skills': extract_skills(jd_tokens, skill_set),
                'experience': extract_experience(jd_text),
                'education': extract_education(jd_text)
            }

            final_score, skill_perc, exp_perc, edu_perc = calculate_match(resume_data, jd_data)

            # Clean up uploaded files
            os.remove(resume_path)
            os.remove(jd_path)

            return render_template('result.html', final_score=final_score, skill_perc=skill_perc, exp_perc=exp_perc, edu_perc=edu_perc)

    return render_template('index.html')

# --------- Run App --------- #
if __name__ == "__main__":
    app.run(debug=True)
