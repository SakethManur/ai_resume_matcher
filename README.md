
📄 Resume vs JD Matcher — Flask App
✨ A smart, lightweight Resume vs Job Description Matcher built with Flask and Natural Language Processing (NLP).

This app automatically analyzes a candidate’s Resume and compares it with a Job Description (JD) based on:

✅ Skills

✅ Experience

✅ Education

It generates a matching score to show how well the resume fits the job profile.

🚀 Features
📄 Upload Resume (PDF) and Job Description (Text) files.

✍️ Auto Extraction:

Skills

Years of Experience

Education

📊 Weighted Match Score:

50% Skills

30% Experience

20% Education

🌐 Simple Flask Web Interface

🤖 Text Preprocessing using spaCy

🛠️ Tech Stack
Python 3.x

Flask — Web framework

pdfplumber — PDF text extraction

spaCy — NLP with en_core_web_sm

HTML/CSS — Frontend templates

📂 Project Structure
plaintext
Copy
Edit
├── app.py
├── templates/
│   ├── index.html
│   └── result.html
├── uploads/
├── requirements.txt
└── README.md
⚙️ Installation and Setup
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/your-username/resume-jd-matcher.git
cd resume-jd-matcher
2. Create a virtual environment (optional but recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Download the spaCy English model
bash
Copy
Edit
python -m spacy download en_core_web_sm
5. Run the Flask app
bash
Copy
Edit
python app.py
6. Open in browser
Visit: http://127.0.0.1:5000/

📋 How to Use
Upload a Resume (PDF).

Upload a Job Description (Text).

Click Submit.

View the Skill Match, Experience Match, Education Match, and the Final Score!

📦 Requirements (requirements.txt)
text
Copy
Edit
Flask
pdfplumber
spacy
(You can generate this via: pip freeze > requirements.txt)

⚡ Future Enhancements
🔍 Smarter skill extraction (phrases, multi-word terms).

🎓 Support multiple degrees (Bachelor’s + Master’s).

🎨 Enhanced UI/UX (responsive and modern).

📄 Add DOCX/other format support.

☁️ Deployment on Heroku or AWS EC2.

🙌 Acknowledgements
Flask

spaCy

pdfplumber

🧑‍💻 Author
Made with ❤️ by Saketh Manur
