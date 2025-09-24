from flask import Flask, request, render_template, jsonify
from utils import classify_and_respond, load_keywords, save_keywords
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
            category, response = classify_and_respond(email_text)
    return render_template("index.html",
                           email_text=email_text,
                           category=category,
                           response=response)

@app.route("/keywords", methods=["GET", "POST"])
def keywords():
    if request.method == "POST":
        prod = [p.strip() for p in request.form.get("produtivo","").split(",") if p.strip()]
        impr = [i.strip() for i in request.form.get("improdutivo","").split(",") if i.strip()]
        save_keywords(prod, impr)
        return jsonify({"status": "ok"})
    prod, impr = load_keywords()
    return jsonify({"produtivo": prod, "improdutivo": impr})

if __name__ == "__main__":
    app.run(debug=True)
