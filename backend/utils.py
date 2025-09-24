# utils.py
import re
import nltk
from transformers import pipeline

# Baixar stopwords portuguesas
nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('portuguese'))

# Palavras-chave para reforço
produtivo_keywords = ["suporte", "atualize", "urgente"]
improdutivo_keywords = ["feliz natal", "obrigado", "saudações"]

# Pipeline de classificação leve (gratuito)
classifier = pipeline(
    "sentiment-analysis",
    model="neuralmind/bert-base-portuguese-cased",
    device=-1  # CPU
)

def preprocess(text):
    """Limpa e normaliza o texto."""
    text = re.sub(r'[^a-zA-ZÀ-ÿ ]', ' ', text)
    words = [w.lower() for w in text.split() if w.lower() not in stop_words]
    return ' '.join(words)

def classify_email(text):
    """
    Classifica o e-mail como Produtivo ou Improdutivo.
    Prioriza palavras-chave de produtividade.
    """
    text_lower = text.lower()
    
    # Se houver qualquer palavra-chave produtiva, considera produtivo
    if any(word in text_lower for word in produtivo_keywords):
        return "Produtivo"
    
    # Se houver palavras improdutivas, mas nenhuma produtiva
    if any(word in text_lower for word in improdutivo_keywords):
        return "Improdutivo"
    
    # Se nenhuma palavra-chave, usa modelo BERT
    preprocessed = preprocess(text)
    result = classifier(preprocessed)[0]
    
    if "positivo" in result['label'].lower():
        return "Produtivo"
    return "Improdutivo"

def generate_response(category, original_text):
    """Gera resposta automática baseada na classificação."""
    if category == "Produtivo":
        return f"Recebemos seu email: Em breve retornaremos com mais informações."
    return f"Obrigado pelo seu contato! Agradecemos sua mensagem."

def classify_and_respond(text):
    """Função única para classificar e gerar resposta."""
    category = classify_email(text)
    response = generate_response(category, text)
    return category, response
