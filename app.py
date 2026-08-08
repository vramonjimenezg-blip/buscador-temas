import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# Configuración visual
st.set_page_config(page_title="Investigador de Avances & Contenido", page_icon="🧠", layout="wide")

st.title("🧠 Buscador de Avances Académicos & Creador de Contenido")
st.caption("Investigación profunda, mapas mentales y carruseles para LinkedIn.")

# Manejo seguro de API Key
api_key = None

# 1. Buscar en los Secretos de Streamlit Cloud
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

# 2. Si no está configurada, mostrar casilla en la barra lateral
with st.sidebar:
    st.header("🔑 Configuración de API")
    if not api_key:
        api_key = st.text_input("Pega tu Gemini API Key aquí:", type="password", help="Obtenla en aistudio.google.com")
        st.info("💡 Pegar tu clave aquí la mantiene 100% segura y evita que GitHub la anule.")

tema = st.text_input("¿Qué tema deseas investigar hoy?", placeholder="Ej. Nuevos avances al crear una Estrategia Comercial...")

PROMPT_MAESTRO = """
ROL: Eres un analista e investigador científico y de negocios internacional. Tu especialidad es la investigación profunda, la triangulación de datos y la divulgación ejecutiva.

TAREA Y FUENTES PERMITIDAS:
1. Analiza e investiga a profundidad el tema: "{TEMA}".
2. RESTRICCIÓN DE FUENTES: Busca ÚNICAMENTE en repositorios y bases de datos académicas/científicas reconocidas (ej. Google Académico, ResearchGate, Academia.edu, ArXiv, SSRN, DOAJ, CORE, Redalyc, SciELO).
3. ALCANCE GLOBAL Y MULTILINGÜE: Rastra publicaciones a nivel mundial sin importar el idioma de origen (incluyendo Asia, Europa, América). Traduce y sintetiza todo al español.
4. TRIANGULACIÓN Y CONTRASTACIÓN: Para CADA UNO de los 5 avances seleccionados, contrasta y valida la información utilizando al menos 2 o 3 artículos o fuentes científicas distintas.

FORMATO DE SALIDA REQUERIDO (Estricto):

---
SECCIÓN 1: MAPA MENTAL
Genera el código Markdown jerárquico:

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

---
SECCIÓN 2: CARRUSEL LINKEDIN

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

---
SECCIÓN 3: BLOG Y LINKEDIN

1. ARTÍCULO PARA BLOG:
   - Redacta un artículo de 350-500 palabras introduciendo el tema y explicando los 5 avances.
   - REFERENCIAS OBLIGATORIAS: Incluye el listado de fuentes con títulos y LINKS directos consultados.

2. COPY PARA LINKEDIN:
   - Redacta el texto para acompañar el carrusel con emoticonos, mención a fuentes académicas y 5 hashtags.
"""

if st.button("🚀 Generar Investigación y Contenido", type="primary"):
    if not tema:
        st.warning("Por favor escribe un tema para investigar.")
    elif not api_key:
        st.error("Por favor ingresa tu API Key en la barra lateral izquierda.")
    else:
        with st.spinner("Investigando fuentes académicas globales y procesando información..."):
            try:
                genai.configure(api_key=api_key.strip())
                
                modelos_a_probar = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-flash']
                response = None
                
                for mod_name in modelos_a_probar:
                    try:
                        model = genai.GenerativeModel(mod_name)
                        prompt_final = PROMPT_MAESTRO.format(TEMA=tema)
                        res_temp = model.generate_content(prompt_final)
                        if res_temp and res_temp.text:
                            response = res_temp
                            break
                    except Exception:
                        continue
                
                if not response:
                    raise Exception("No se pudo conectar con Gemini. Verifica que tu clave de Google AI Studio esté activa.")

                texto_resultado = response.text
                st.success("¡Investigación completada con éxito!")
                
                partes = texto_resultado.split("---")
                tab1, tab2, tab3 = st.tabs(["🗺️ Mapa Mental", "📱 Carrusel LinkedIn", "📝 Blog & Copy"])
                
                with tab1:
                    st.subheader("Mapa Mental de Asimilación Rápida")
                    sec1 = partes[1] if len(partes) > 1 else texto_resultado
                    st.markdown(sec1)
                    
                    markmap_html = f"""
                    <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader"></script>
                    <div class="markmap">
                    {sec1.replace('SECCIÓN 1: MAPA MENTAL', '')}
                    </div>
                    """
                    components.html(markmap_html, height=450, scrolling=True)
                    
                with tab2:
                    st.subheader("Guion Estructurado para Carrusel (8 Láminas)")
                    sec2 = partes[2] if len(partes) > 2 else "No se pudo formatear la sección 2."
                    st.text_area("Copia este guion para Canva:", value=sec2, height=400)
                    
                with tab3:
                    st.subheader("Artículo para Blog y Post de LinkedIn")
                    sec3 = partes[3] if len(partes) > 3 else "No se pudo formatear la sección 3."
                    st.markdown(sec3)
                    
            except Exception as e:
                st.error(f"Error al procesar: {e}")
