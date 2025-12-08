import streamlit as st
import subprocess

@st.cache_resource
def install_camoufox():
    try:
        subprocess.run(["python", "-m", "camoufox", "fetch"])
        print("Camoufox installed successfully.")
    except Exception as e:
        print(f"Error installing Camoufox: {e}")
    