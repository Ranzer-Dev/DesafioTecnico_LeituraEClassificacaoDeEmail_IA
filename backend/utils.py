import re, nltk, json, os
from transformers import pipeline

nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('portuguese'))

KEYWORDS_FILE = os.path.join(os.path.dirname(__file__), "keywords.json")

def load_keywords():
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("produtivo", []), data.get("improdutivo", [])
    # valores padrão
    return ["suporte", "atualize", "urgente"], ["feliz natal", "obrigado", "saudações"]

def save_keywords(produtivo_list, improdutivo_list):
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "produtivo": produtivo_list,
            "improdutivo": improdutivo_list
        }, f, ensure_ascii=False, indent=4)

classifier = pipeline(
    "sentiment-analysis",
    model="neuralmind/bert-base-portuguese-cased",
    device=-1
)

def preprocess(text):
    text = re.sub(r'[^a-zA-ZÀ-ÿ ]', ' ', text)
    words = [w.lower() for w in text.split() if w.lower() not in stop_words]
    return ' '.join(words)

def classify_email(text):
    produtivo_keywords, improdutivo_keywords = load_keywords()
    lower = text.lower()
    if any(w in lower for w in produtivo_keywords):
        return "Produtivo"
    if any(w in lower for w in improdutivo_keywords):
        return "Improdutivo"
    result = classifier(preprocess(text))[0]
    return "Produtivo" if "positivo" in result['label'].lower() else "Improdutivo"

def generate_response(category, original_text):
    return ("Recebemos seu email: Em breve retornaremos com mais informações."
            if category == "Produtivo"
            else "Obrigado pelo seu contato! Agradecemos sua mensagem.")

def classify_and_respond(text):
    cat = classify_email(text)
    return cat, generate_response(cat, text)
