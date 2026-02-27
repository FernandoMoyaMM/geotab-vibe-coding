import streamlit as st
import os
import time
from google import genai
from dotenv import load_dotenv

# --- SECURE CONFIGURATION LOADING ---
load_dotenv()
# --- ENVIRONMENT CONFIGURATION ---
PROJECT_ID = os.getenv("PROJECT_ID")

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Geotab Support AI", 
    page_icon="🤖", 
    layout="centered"
)

@st.cache_resource
def inicializar_clientes():
    """Creates Gemini client using PROJECT_ID from .env."""
    if not PROJECT_ID:
        st.error("❌ PROJECT_ID not found in .env file")
        st.stop()
        
    try:
        # SDK automatically detects GO_APPLICATION_CREDENTIALS if the variable exists
        genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
        return genai_client
    except Exception as e:
        st.error(f"❌ Error connecting to Google Cloud: {e}")
        st.stop()

genai_client = inicializar_clientes()

# --- SESSION STATE (MEMORY) ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = genai_client.chats.create(model="gemini-2.0-flash")
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- VISUAL INTERFACE (Header) ---
header_container = st.container()
with header_container:
    col1, col2 = st.columns([1, 4])
    with col1:
        if os.path.exists("icono_geotab.jpg"):
            st.image("icono_geotab.jpg", width=80)
        else:
            st.write("🤖") 
    with col2:
        st.title("Support Geotab")
        st.caption("AI Technical Support Assistant - GO9 & GO Focus")

st.markdown("---")

# Sidebar for utilities
with st.sidebar:
    if os.path.exists("icono_geotab.jpg"):
        st.image("icono_geotab.jpg", use_container_width=True)
    
    st.header("Control Panel")
    if st.button("🗑️ New Consultation"):
        st.session_state.messages = []
        st.session_state.chat_session = genai_client.chats.create(model="gemini-2.0-flash")
        st.rerun()
    
    st.divider()
    st.info(f"**Active Project:**\n{PROJECT_ID}")
    st.info("Source: Official Geotab Documentation")

# Display message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- MAIN FLOW ---
if prompt := st.chat_input("E.g.: What do the red, green, and blue LEDs mean?"):
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- ROUTING LOGIC (GO9 vs GO FOCUS) ---
    URL_GO9 = "https://www.geotab.com/es/go9-support-document/"
    URL_FOCUS = "https://support.geotab.com/camera-devices/doc/go-focus-plus-new"
    
    # Detectamos si el usuario pregunta por la cámara Focus
    prompt_lower = prompt.lower()
    if "focus" in prompt_lower:
        url_soporte = URL_FOCUS
        target_device = "GO Focus / Focus Plus"
    else:
        url_soporte = URL_GO9
        target_device = "Geotab GO9"

    # 2. Status Update (Simplified since we removed the web scraper)
    with st.status(f"🧠 Analyzing {target_device} documentation...", expanded=False) as status:
        st.write(f"Directing query to: {target_device} technical base.")
        st.write(f"Reference URL: {url_soporte}")
        status.update(label=f"Ready for {target_device} query", state="complete")

    # 3. Response with Gemini
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # --- REFUERZO DE IDIOMA Y CONTEXTO ---
        # Ahora el modelo usará su base de conocimiento interna pero guiado por la URL de referencia
        instruccion_maestra = f"""
        You are a Geotab Technical Support Expert specializing in {target_device}. 
        
        STRICT MANDATE:
        - Your output must ALWAYS be in English. No exceptions.
        - If the user asks in Spanish, translate your answer to English.
        - Base your technical answers on the official Geotab standards for {target_device}.
        - Reference this documentation URL in your response if helpful: {url_soporte}
        """

        try:
            # Forzamos la respuesta en inglés mediante un prefijo
            prompt_final = f"{instruccion_maestra}\n\nUSER QUESTION: {prompt}\n\nTECHNICAL ANSWER IN ENGLISH:"
            
            response = st.session_state.chat_session.send_message(prompt_final)
            texto_completo = response.text
            
            # Typing effect
            for i in range(len(texto_completo)):
                full_response = texto_completo[:i+1]
                placeholder.markdown(full_response + "▌")
                time.sleep(0.001)
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error generating response: {e}")