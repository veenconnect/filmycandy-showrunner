import streamlit as st
import google.generativeai as genai
import importlib.metadata

st.title("🛠️ System Check Mode")

# 1. Check Library Version (Isse pata chalega requirements.txt kaam kiya ya nahi)
try:
    version = importlib.metadata.version("google-generativeai")
    st.write(f"📂 Installed Software Version: **{version}**")
    
    if version < "0.7.2":
        st.error("❌ Version PURANA hai! requirements.txt file ka naam check karein.")
    else:
        st.success("✅ Version NAYA hai! Software updated hai.")
except:
    st.error("⚠️ Library hi nahi mili!")

# 2. Check API Key & Models
api_key = st.text_input("Apni Gemini API Key yahan daalein:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        st.write("🔍 Google se models ki list mangwa rahe hain...")
        
        models = genai.list_models()
        found = False
        st.write("### Available Models for your Key:")
        
        for m in models:
            st.write(f"- `{m.name}`")
            if "flash" in m.name:
                found = True
        
        if found:
            st.success("🎉 'Flash' model available hai! Ab hum asli app chala sakte hain.")
        else:
            st.error("🚫 Aapki Key par 'Flash' model nahi dikh raha. Nayi Key leni pad sakti hai.")
            
    except Exception as e:
        st.error(f"Error: {e}")
