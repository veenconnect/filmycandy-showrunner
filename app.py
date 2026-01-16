import streamlit as st
import google.generativeai as genai
from prompt_data import system_prompt

# Page Configuration
st.set_page_config(page_title="Filmycandy AI Showrunner", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🎬 Filmycandy Setup")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.markdown("---")
    st.write("Powered by Google Gemini 1.5 Flash")
    
    # Reset Button
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.rerun()

# Main App Title
st.title("🎬 AI Showrunner: Haresh Jen Togani")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Check for API Key
if not api_key:
    st.warning("⚠️ Please enter your Google Gemini API Key to start.")
    st.stop()

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    
    # Configuration for the model
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

    # Initialize Model - Using the standard stable version
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_prompt
    )
except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

# Display Chat History
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# User Input Logic
if user_input := st.chat_input("Apna jawab ya idea yahan likhein..."):
    # 1. User message display
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # History conversion
            chat_history = []
            for msg in st.session_state.messages[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                chat_history.append({"role": role, "parts": [msg["content"]]})
            
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(user_input, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "model", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
