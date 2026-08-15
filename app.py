import google.generativeai as genai
import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Investigador de Avances & Contenido",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Buscador de Avances Académicos & Creador de Contenido")
st.caption(
    "Investigación profunda, mapas mentales interactivos y carruseles para"
    " LinkedIn."
)

# 1. Obtener la API Key (prioridad: Secrets de Streamlit > Barra lateral)
api_key = ""
try:
  if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
  pass

with st.sidebar:
  st.header("🔑 Configuración")
  if not api_key:
    api_key = st.text_input(
        "Pega tu Gemini API Key aquí:",
        type="password",
        help="Consíguela gratis en https://aistudio.google.com",
    )
    st.info("💡 Pegar tu clave aquí no la guarda de forma permanente.")
  else:
    st.success("✅ Clave de API detectada automáticamente.")

tema = st.text_input(
    "¿Qué tema deseas investigar hoy?",
    placeholder="Ej. Estrategias comerciales impulsadas por Inteligencia Artificial en B2B...",
)

PROMPT_MAESTRO = """
ROL: Eres un analista e investigador científico y de negocios internacional. Tu especialidad es la investigación profunda, la triangulación de datos y la divulgación ejecutiva.

TAREA Y FUENTES PERMITIDAS:
1. Analiza e investiga a profundidad el tema: "{TEMA}".
2. RESTRICCIÓN DE FUENTES: Busca ÚNICAMENTE en repositorios y bases de datos académicas/científicas reconocidas (ej. Google Académico, ResearchGate, Academia.edu, ArXiv, SSRN, DOAJ, Redalyc, SciELO).
3. ALCANCE GLOBAL Y MULTILINGÜE: Rastrea publicaciones a nivel mundial sin importar el idioma de origen. Traduce y sintetiza todo al español.
4. TRIANGULACIÓN Y CONTRASTACIÓN: Para CADA UNO de los 5 avances seleccionados, contrasta y valida la información utilizando al menos 2 o 3 fuentes científicas distintas.

FORMATO DE SALIDA REQUERIDO (Usa estrictamente las marcas [SECCION_1], [SECCION_2], [SECCION_3] para dividir el contenido):

[SECCION_1]
# {TEMA}
## 1. [Nombre del Avance 1]
- Concepto: [Explicación breve]
- Impacto: [Impacto práctico]
- Evidencia: [Síntesis contrastada]
## 2. [Nombre del Avance 2]
- Concepto: [Explicación breve]
- Impacto: [Impacto práctico]
- Evidencia: [Síntesis contrastada]
## 3. [Nombre del Avance 3]
- Concepto: [Explicación breve]
- Impacto: [Impacto práctico]
- Evidencia: [Síntesis contrastada]
## 4. [Nombre del Avance 4]
- Concepto: [Explicación breve]
- Impacto: [Impacto práctico]
- Evidencia: [Síntesis contrastada]
## 5. [Nombre del Avance 5]
- Concepto: [Explicación breve]
- Impacto: [Impacto práctico]
- Evidencia: [Síntesis contrastada]

[SECCION_2]
* LÁMINA 1 (PORTADA):
  - Titular Principal: [Título persuasivo]
  - Subtítulo: [Resumen en 1 línea]

* LÁMINA 2 (CONTEXTO GLOBAL):
  - Mensaje clave: [Contexto mundial]

* LÁMINAS 3 A 7 (LOS 5 AVANCES):
  - [Genera 1 sección por avance con: Número + Título, Concepto e Impacto]

* LÁMINA 8 (CIERRE/CTA):
  - Pregunta: [Para debate]
  - CTA: 💾 Guarda este análisis | 🔄 Comparte | 💬 Opina abajo

[SECCION_3]
1. ARTÍCULO PARA BLOG:
   - Redacta un artículo de 350-500 palabras introduciendo el tema y explicando los 5 avances.
   - REFERENCIAS OBLIGATORIAS: Incluye el listado de fuentes con títulos y enlaces consultados.

2. COPY PARA LINKEDIN:
   - Redacta el texto para acompañar el carrusel con emoticonos, mención a fuentes académicas y 5 hashtags.
"""

if st.button("🚀 Generar Investigación y Contenido", type="primary"):
  if not tema:
    st.warning("⚠️ Por favor escribe un tema para investigar.")
  elif not api_key:
    st.error("⚠️ Por favor ingresa tu Gemini API Key en la barra lateral.")
  else:
    with st.spinner(
        "🔎 Investigando fuentes académicas globales y procesando"
        " información..."
    ):
      try:
        # Configurar la API
        genai.configure(api_key=api_key.strip())

        # Probar modelos compatibles
        modelos = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
        respuesta_texto = None
        ultimo_error = None

        for nombre_modelo in modelos:
          try:
            model = genai.GenerativeModel(nombre_modelo)
            prompt_final = PROMPT_MAESTRO.format(TEMA=tema)
            response = model.generate_content(prompt_final)
            if response and response.text:
              respuesta_texto = response.text
              break
          except Exception as e:
            ultimo_error = e
            continue

        if not respuesta_texto:
          st.error(f"❌ Error al conectar con la API de Gemini: {ultimo_error}")
        else:
          st.success("✨ ¡Investigación completada con éxito!")

          # Extraer secciones de manera segura
          sec1 = ""
          sec2 = ""
          sec3 = ""

          if "[SECCION_1]" in respuesta_texto:
            partes = respuesta_texto.split("[SECCION_1]")
            resto = partes[1] if len(partes) > 1 else ""

            if "[SECCION_2]" in resto:
              p_sec1, resto2 = resto.split("[SECCION_2]", 1)
              sec1 = p_sec1.strip()

              if "[SECCION_3]" in resto2:
                sec2, sec3 = resto2.split("[SECCION_3]", 1)
                sec2 = sec2.strip()
                sec3 = sec3.strip()
              else:
                sec2 = resto2.strip()
            else:
              sec1 = resto.strip()
          else:
            sec1 = respuesta_texto

          # Mostrar Pestañas
          tab1, tab2, tab3 = st.tabs(
              ["🗺️ Mapa Mental", "📱 Carrusel LinkedIn", "📝 Blog & Copy"]
          )

          with tab1:
            st.subheader("Mapa Mental de Asimilación Rápida")
            st.markdown(sec1)

            # Visor visual Markmap
            markmap_html = f"""
                        <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader"></script>
                        <div class="markmap" style="height: 400px;">
                        {sec1}
                        </div>
                        """
            components.html(markmap_html, height=450, scrolling=True)

          with tab2:
            st.subheader("Guión Estructurado para Carrusel (Canva)")
            st.text_area(
                "Copia y pega este contenido en Canva o tu diseñador:",
                value=sec2 if sec2 else "No se pudo formatear el carrusel.",
                height=400,
            )

          with tab3:
            st.subheader("Artículo para Blog y Post de LinkedIn")
            st.markdown(
                sec3
                if sec3
                else "No se pudo formatear la sección de Blog & Copy."
            )

      except Exception as ex:
        st.error(f"❌ Ocurrió un detalle inesperado: {ex}")
