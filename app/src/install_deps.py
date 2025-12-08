import streamlit as st
import subprocess

@st.cache_resource
def install_camoufox():
    try:
        subprocess.run(["uv", "sync"])
        subprocess.run(["uv", "add", "pydantic"])
        subprocess.run(["uv", "add", "camoufox"])
        print("Dependencies installed successfully.")
    except Exception as e:
        print(f"Error installing dependencies: {e}")
    