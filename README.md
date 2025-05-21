# 🔍 Resume Matcher – Intelligent Resume Screening Application

## 📌 Overview

**Resume Matcher** is an AI-powered web application built with **Flask** that automates the comparison of candidate resumes against job descriptions (JDs). By leveraging **Natural Language Processing (NLP)** with **spaCy**, the application extracts and analyzes core components such as skills, experience, and education from PDF resumes and `.txt` job descriptions to compute a **match score**.

This tool streamlines the **pre-screening process** in recruitment pipelines, helping HR professionals and hiring managers make informed decisions faster.

---

## 🚀 Key Features

- 📄 **PDF Resume Parsing** using `pdfplumber`
- 🧠 **NLP-based Preprocessing** with `spaCy` (tokenization, lemmatization, stop-word removal)
- 🛠️ **Keyword-based Skill Extraction** from a predefined technical skill set (e.g., Python, SQL, AWS, React)
- 📊 **Quantitative Match Scoring**:
  - **Skill Match**
  - **Experience Match**
  - **Education Match**
- 🎯 **Final Weighted Score** based on configurable weights (skills: 50%, experience: 30%, education: 20%)
- 📈 **Responsive Frontend** using `Bootstrap` and modern UI/UX design
- 📥 Upload interface for resume (PDF) and job description (TXT)
- 💡 Dynamic feedback (Excellent, Good, or Needs Improvement) based on match score thresholds

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask
- **NLP**: spaCy (`en_core_web_sm`)
- **PDF Processing**: pdfplumber
- **Frontend**: HTML, CSS, Bootstrap 5
- **File Handling**: Secure uploads with `os` module
- **Regex**: Experience and education extraction using pattern matching

---

## 🧪 How It Works

1. **User uploads** a resume (PDF) and a job description (TXT).
2. The system:
   - Parses and tokenizes both documents.
   - Extracts skills, experience, and education credentials.
3. **Score calculation** is performed based on:
   - Skills overlap with JD
   - Experience years relative to JD requirement
   - Education match
4. **Results rendered** via `result.html` with detailed percentage scores and a user-friendly recommendation.

---

## 📦 Dependencies

Install via `pip install -r requirement.txt`:

```
Flask
pdfplumber
spacy
```

> Also ensure the spaCy model is downloaded:

```bash
python -m spacy download en_core_web_sm
```

---

## 🧑‍💻 Usage

Run the Flask application:

```bash
python app.py
```

Open `http://localhost:5000` in your browser to start matching resumes against JDs.

---

## 📁 File Structure

```
.
├── app.py                 # Main Flask backend logic
├── requirement.txt        # Python dependencies
├── index.html             # Upload UI (Resume + JD)
├── result.html            # Match results display
```

## 📬 Feedback

This application is ideal for building HR tech solutions or resume-filtering systems in recruitment software.

🧑‍💻 Author
Made with ❤️ by Saketh Manur
