import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import streamlit.components.v1 as components

st.set_page_config(page_title="Investigador de Avances & Contenido", page_icon="", layout="wide")
st.title("Buscador de Avances Académicos & Creador de Contenido")
st.caption("Investigación profunda, mapas mentales y carruseles para LinkedIn (HuggingFace CPU).")

@st.cache_resource
def cargar_modelo():
    modelo = "Qwen/Qwen2.5-1.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(modelo)
    model = AutoModelForCausalLM.from_pretrained(modelo, torch_dtype=torch.float32)
    return tokenizer, model

tokenizer, model = cargar_modelo()

tema = st.text_input("¿Qué tema deseas investigar hoy?", placeholder="Ej. Nuevos avances al crear una Estrategia Comercial ...")

PROMPT_MAESTRO = """
Genera un análisis completo sobre el tema: "{TEMA}"

Incluye estrictamente:

---
SECCIÓN 1: MAPA MENTAL
# {TEMA}
## 1. Avance 1
- Concepto:
- Impacto:
- Evidencia:
## 2. Avance 2
- Concepto:
- Impacto:
- Evidencia:
## 3. Avance 3
- Concepto:
- Impacto:
- Evidencia:
## 4. Avance 4
- Concepto:
- Impacto:
- Evidencia:
## 5. Avance 5
- Concepto:
- Impacto:
- Evidencia:

---
SECCIÓN 2: CARRUSEL LINKEDIN
Genera 8 láminas:
1. Portada
2. Contexto global
3-7. Avances
8. Cierre y CTA

---
SECCIÓN 3: BLOG Y COPY
- Artículo de 350-500 palabras
- Copy para LinkedIn con hashtags
"""

def generar_respuesta(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=1500,
        temperature=0.7
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if st.button("Generar Investigación y Contenido", type="primary"):
    if not tema:
        st.warning("Por favor escribe un tema para investigar.")
    else:
        with st.spinner("Generando contenido con Qwen (HuggingFace CPU)..."):
            prompt_final = PROMPT_MAESTRO.format(TEMA=tema)
            texto_resultado = generar_respuesta(prompt_final)

            partes = texto_resultado.split("---")
            tab1, tab2, tab3 = st.tabs(["Mapa Mental", "Carrusel LinkedIn", "Blog & Copy"])

            with tab1:
                st.subheader("Mapa Mental")
                sec1 = partes[1] if len(partes) > 1 else texto_resultado
                st.markdown(sec1)

            with tab2:
                st.subheader("Guion para Carrusel")
                sec2 = partes[2] if len(partes) > 2 else "No se pudo formatear la sección 2."
                st.text_area("Copia este guion para Canva:", value=sec2, height=400)

            with tab3:
                st.subheader("Artículo y Copy")
                sec3 = partes[3] if len(partes) > 3 else "No se pudo formatear la sección 3."
                st.markdown(sec3)
