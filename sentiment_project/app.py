import streamlit as st
from sentiment import analyze_sentiments

st.set_page_config(page_title="Análisis de Sentimientos", page_icon="🧠")

st.title("🧠 Análisis de Sentimientos con Hilos en Paralelo")
st.write("Sube un archivo `.txt` con comentarios (uno por línea) para analizar su sentimiento.")

# Cargar archivo de texto
uploaded = st.file_uploader("Selecciona un archivo", type=["txt"])

# Si el usuario carga un archivo
if uploaded is not None:
    # Leer líneas y limpiar
    comments = [l.strip() for l in uploaded.read().decode('utf-8').splitlines() if l.strip()]

    # Mostrar cantidad
    st.success(f"✅ {len(comments)} comentarios cargados correctamente.")

    # Ejecutar análisis con hilos
    with st.spinner("Analizando sentimientos en paralelo..."):
        results = analyze_sentiments(comments)

    # Mostrar resultados
    st.write("### 📊 Resultados del análisis")
    st.dataframe(results)

    # Contar resumen de resultados
    counts = results['sentiment'].value_counts()
    st.write("### 📈 Resumen:")
    st.bar_chart(counts)

else:
    st.info("Por favor, sube un archivo .txt para comenzar.")

