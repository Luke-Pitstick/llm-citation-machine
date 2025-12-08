import streamlit as st
import subprocess

@st.cache_resource
def install_camoufox():
    try:
        subprocess.run(["uv", "sync"])
        subprocess.run(["uv", "add", "pydantic"])
        subprocess.run(["pip", "install", "pydantic"])
        #subprocess.run(["pip", "install", "camoufox"])
        subprocess.run(["pip", "-m", "camoufox", "fetch"])
        
        print("Dependencies installed successfully.")
        
    except Exception as e:
        print(f"Error installing dependencies: {e}")
    