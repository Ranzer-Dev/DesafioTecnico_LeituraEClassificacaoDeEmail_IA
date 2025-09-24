#app.py

from flask import Flask, request, render_template
from utils import classify_and_respond
import os
from PyPDF2 import PdfReader
from docx import Document

app = Flask(__name__, template_folder="../frontend", static_folder="../frontend")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_file(file_path):
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return ""

@app.route("/", methods=["GET", "POST"])
def index():
    category = ""
    response = ""
    email_text = ""

    if request.method == "POST":
        # Receber texto direto
        email_text = request.form.get("email_text", "")

        # Receber arquivo
        file = request.files.get("email_file")
        if file:
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            email_text = extract_text_from_file(filename)

        if email_text:
            category, response = classify_and_respond(email_text)

    return render_template("index.html",
                           email_text=email_text,
                           category=category,
                           response=response)

if __name__ == "__main__":
    app.run(debug=True)
