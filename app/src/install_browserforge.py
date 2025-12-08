import os
import sys
from pathlib import Path
import requests
import subprocess
import streamlit as st

@st.cache_resource
def install_browserforge():
    # Set custom data directory in a writable location
    DATA_DIR = Path("/tmp/browserforge_data")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Set environment variable before importing browserforge
    os.environ["BROWSERFORGE_DATA_DIR"] = str(DATA_DIR)

    
    subprocess.run(["pip", "install", "browserforge[all]"])

    print(f"BrowserForge data directory set to: {DATA_DIR}")
    print(f"Files downloaded: {list(DATA_DIR.glob('*.zip'))}")