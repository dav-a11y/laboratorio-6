import concurrent.futures
import threading
import pandas as pd

# Diccionarios de palabras clave
positive_words = ["excelente", "bueno", "genial", "positivo", "feliz", "maravilloso", "fantástico", "increíble"]
negative_words = ["malo", "horrible", "terrible", "negativo", "triste", "pésimo", "decepcionante", "defectuoso"]

lock = threading.Lock()

# --- Analizador simple de sentimiento ---
def analyze_sentiment(text):
    text = text.lower()
    score = 0
    for word in positive_words:
        if word in text:
            score += 1
    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        return "positivo"
    elif score < 0:
        return "negativo"
    else:
        return "neutro"

# --- Función para procesar en paralelo ---
def analyze_sentiments(comments):
    results = []

    def process_comment(comment):
        sentiment = analyze_sentiment(comment)
        with lock:
            results.append({"comment": comment, "sentiment": sentiment})

    # Ejecutar hilos en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_comment, comments)

    return pd.DataFrame(results)
