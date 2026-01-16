import streamlit as st
import openai
from prompt_data import system_prompt

# Page Configuration
st.set_page_config(page_title="Filmycandy AI Showrunner", layout="wide")

# Sidebar for API Key
with st.sidebar:
    st.title("🎬 Filmycandy Setup")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.markdown("---")
    st.write("Production: Filmycandy Entertainment")
    
    # Reset Button
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.rerun()

# Main App Title
st.title("🎬 AI Showrunner: Haresh Jen Togani")
st.markdown("### Professional OTT Content Architect")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add the System Prompt invisibly
    st.session_state.messages.append({"role": "system", "content": system_prompt})

# Check for API Key
if not api_key:
    st.warning("⚠️ Please enter your OpenAI API Key in the sidebar to start.")
    st.stop()

# Configure OpenAI Client
client = openai.OpenAI(api_key=api_key)

# Display Chat History (Excluding System Prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input Logic
if user_input := st.chat_input("Apna jawab ya idea yahan likhein..."):
    # 1. User ka message dikhao
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # 2. History mein add karo
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 3. AI se response mango
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Call GPT-4o model (Powerful enough for your logic)
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            
            # Response stream karo (Typing effect)
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # 4. AI ka response history mein save karo
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
