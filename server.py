import os

from flask import Flask, render_template, request

from utils.matcher import match_resumes
from utils.resume_parser import extract_text
from utils.suggestor import suggest_improvements

UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        job_description = request.form["job_description"]
        resume_files = request.files.getlist("resumes")
        results = []

        for resume in resume_files:
            # Save uploaded resume
            path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
            resume.save(path)

            # Extract text from resume (for AI suggestions)
            resume_text = extract_text(path)

            # Match score using file path
            score = match_resumes([path], job_description)[0]

            # Generate AI suggestions
            suggestions = suggest_improvements(resume_text, job_description)

            # Append all info for rendering
            results.append({
                "filename": resume.filename,
                "score": score,
                "text": resume_text,
                "suggestions": suggestions
            })

        return render_template("results.html", results=results, jd=job_description)

    return render_template("index.html")


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
