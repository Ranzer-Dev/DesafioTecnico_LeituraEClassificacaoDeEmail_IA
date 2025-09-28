from flask import Flask, request, render_template
from utils import gerar_resposta_complexa

import os
from PyPDF2 import PdfReader
from docx import Document

app = Flask(__name__, template_folder="../frontend", static_folder="../frontend")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_file(path):
    if path.endswith(".txt"):
        return open(path, encoding="utf-8").read()
    elif path.endswith(".pdf"):
        return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)
    elif path.endswith(".docx"):
        return "\n".join(p.text for p in Document(path).paragraphs)
    return ""

@app.route("/", methods=["GET", "POST"])
def index():
    category, response, email_text = "", "", ""
    if request.method == "POST":
        email_text = request.form.get("email_text", "")
        file = request.files.get("email_file")
        if file:
            fname = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(fname)
            email_text = extract_text_from_file(fname)
        if email_text:
            response = gerar_resposta_complexa(email_text)
            category = "Produtivo" if "PRODUTIVO" in response.upper() else "Improdutivo"
    return render_template("index.html", email_text=email_text, category=category, response=response)

if __name__ == "__main__":
    app.run(debug=True)
