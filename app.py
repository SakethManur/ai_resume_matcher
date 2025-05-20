# app.py

from flask import Flask, render_template, request, jsonify
import os
import tempfile
import pdfplumber
import spacy
import re
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add file handler for logging
log_dir = os.path.join(tempfile.gettempdir(), 'resume_matcher_logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'resume_matcher.log')
file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
logger.info('Resume Matcher startup')

# Use temporary directory for uploads in serverless environment
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load Spacy model
try:
    nlp = spacy.load('en_core_web_sm')
    logger.info('Successfully loaded spaCy model')
except OSError:
    logger.warning('spaCy model not found, downloading now...')
    os.system('python -m spacy download en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')
    logger.info('Successfully downloaded and loaded spaCy model')

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
    match = re.search(r'(\d+)\s*\+?\s*(?:years|yrs)', text.lower())
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
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    logger.info('Received analyze request')
    resume = request.files['resume']
    job_description = request.form['job_description']
    job_title = request.form['job_title']
    required_skills = request.form['required_skills']
    required_experience = request.form.get('required_experience', '0')
    required_education = request.form.get('required_education', '')

    if not all([resume, job_description, job_title, required_skills]):
        logger.error('Missing required fields in request')
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        resume.save(resume_path)
        logger.info(f'Successfully saved resume: {resume.filename}')

        resume_text = extract_text_from_pdf(resume_path)
        logger.info('Successfully extracted text from PDF')

        # Combine job title and description for better context
        jd_text = f"Job Title: {job_title}\n\nRequired Skills: {required_skills}\n\nExperience Required: {required_experience} years\n\nEducation Required: {required_education}\n\nJob Description:\n{job_description}"

        skill_set = { "python", "java", "sql", "machine learning", "data analysis", "aws", "docker",
                    "react", "c++", "cloud", "html", "css", "javascript", "typescript", "nodejs",
                    "angular", "flask", "django", "kubernetes", "git", "github", "tensorflow",
                    "pytorch", "scikit-learn", "numpy", "pandas", "matplotlib", "seaborn"}

        resume_tokens = preprocess(resume_text)
        jd_tokens = preprocess(jd_text)
        logger.info('Successfully preprocessed resume and job description')

        resume_data = {
            'skills': extract_skills(resume_tokens, skill_set),
            'experience': extract_experience(resume_text),
            'education': extract_education(resume_text)
        }
        logger.info(f'Extracted resume data: {resume_data}')

        jd_data = {
            'skills': extract_skills(jd_tokens, skill_set),
            'experience': extract_experience(jd_text),
            'education': extract_education(jd_text)
        }
        logger.info(f'Extracted job description data: {jd_data}')

        final_score, skill_perc, exp_perc, edu_perc = calculate_match(resume_data, jd_data)
        logger.info(f'Calculated scores - Final: {final_score}, Skills: {skill_perc}, Experience: {exp_perc}, Education: {edu_perc}')

        # Clean up uploaded file
        os.remove(resume_path)
        logger.info('Cleaned up temporary files')

        return jsonify({
            'final_score': round(final_score, 2),
            'skill_perc': round(skill_perc, 2),
            'exp_perc': round(exp_perc, 2),
            'edu_perc': round(edu_perc, 2)
        })
    except Exception as e:
        logger.error(f'Error processing request: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 400

# --------- Run App --------- #
if __name__ == "__main__":
    logger.info('Starting Flask app')
    app.run(debug=True)
