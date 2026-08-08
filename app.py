import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# Configuración visual de la página
st.set_page_config(page_title="Investigador de Avances & Contenido", page_icon="🧠", layout="wide")

st.title("🧠 Buscador de Avances Académicos & Creador de Contenido")
st.caption("Investigación profunda, mapas mentales y carruseles para LinkedIn a presupuesto $0.")

# Campo para que el usuario ingrese su API Key de Gemini
api_key = st.sidebar.text_input("Ingresa tu Gemini API Key:", type="password")

# Campo para ingresar el tema a investigar
tema = st.text_input("¿Qué tema deseas investigar hoy?", placeholder="Ej. Inteligencia Artificial en Finanzas, Nanotecnología en Salud...")

# Prompt Maestro Definitivo integrado
PROMPT_MAESTRO = """
ROL: 
Eres un analista e investigador científico y de negocios internacional. Tu especialidad es la investigación profunda, la triangulación de datos y la divulgación ejecutiva.

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
    if not api_key:
        st.error("Por favor ingresa tu API Key de Gemini en la barra lateral.")
    elif not tema:
        st.warning("Por favor escribe un tema para investigar.")
    else:
        with st.spinner("Investigando fuentes académicas globales y procesando información..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt_final = PROMPT_MAESTRO.format(TEMA=tema)
                response = model.generate_content(prompt_final)
                texto_resultado = response.text
                
                st.success("¡Investigación completada con éxito!")
                
                # Separar las secciones
                partes = texto_resultado.split("---")
                
                tab1, tab2, tab3 = st.tabs(["🗺️ Mapa Mental", "📱 Carrusel LinkedIn", "📝 Blog & Copy"])
                
                with tab1:
                    st.subheader("Mapa Mental de Asimilación Rápida")
                    sec1 = partes[1] if len(partes) > 1 else texto_resultado
                    st.markdown(sec1)
                    
                    # Generación de mapa mental gráfico HTML interactivo mediante Markmap
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
                st.error(f"Ocurrió un error al conectar con Gemini: {e}")