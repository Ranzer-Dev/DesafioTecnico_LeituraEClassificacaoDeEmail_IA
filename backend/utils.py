import re, nltk, json, os
from transformers import pipeline
import requests

nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('portuguese'))

def preprocess(text):
    text = re.sub(r'[^a-zA-ZÀ-ÿ ]', ' ', text)
    words = [w.lower() for w in text.split() if w.lower() not in stop_words]
    return ' '.join(words)

def gerar_resposta_complexa(email_text):
    prompt = f"""Você é um assistente que analisa e-mails recebidos pela empresa.
Classifique se é PRODUTIVO ou IMPRODUTIVO e depois escreva uma resposta formal e completa em português.

E-mail:
\"\"\"{email_text}\"\"\""""

    # Usa stream=True para ler linha a linha
    with requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "options": {
                "temperature": 0.3,
                "num_predict": 150   # limite de tokens de saída
            }
        },
        stream=True,
    ) as r:
        ...
        r.raise_for_status()
        resposta = []
        for line in r.iter_lines():
            if line:
                try:
                    obj = json.loads(line.decode("utf-8"))
                    # cada objeto tem a chave 'response' com um pedaço do texto
                    if "response" in obj:
                        resposta.append(obj["response"])
                except json.JSONDecodeError:
                    # ignora linhas que não sejam JSON válido
                    continue
    return "".join(resposta).strip()


def classify_and_respond(texto):
    resposta = gerar_resposta_complexa(texto)
    # se quiser ainda extrair a categoria:
    categoria = "Produtivo" if "PRODUTIVO" in resposta.upper() else "Improdutivo"
    return categoria, resposta

