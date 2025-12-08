import os
import sys
from pathlib import Path
import requests
import streamlit as st

@st.cache_resource
def install_browserforge():
    # Set custom data directory
    DATA_DIR = Path("/tmp/browserforge_data")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # The data files are now in a separate PyPI package
    # But if you need to download them manually, use the raw GitHub URLs
    files = {
        "fingerprint-network.zip": "https://raw.githubusercontent.com/daijro/browserforge/main/browserforge/fingerprints/data/fingerprint-network.zip",
        "input-network.zip": "https://raw.githubusercontent.com/daijro/browserforge/main/browserforge/headers/data/input-network.zip"
    }

    # Alternative: Use the apify package directly
    try:
        from apify_fingerprint_datapoints import get_fingerprint_network
        print("apify_fingerprint_datapoints is available!")
    except ImportError:
        print("Need to install apify_fingerprint_datapoints")

    for filename, url in files.items():
        filepath = DATA_DIR / filename
        if not filepath.exists():
            print(f"Downloading {filename} from {url}...")
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                filepath.write_bytes(response.content)
                print(f"Successfully saved {filename}")
            except Exception as e:
                print(f"Failed to download {filename}: {e}")
        else:
            print(f"{filename} already exists at {filepath}")

    os.environ["BROWSERFORGE_DATA_DIR"] = str(DATA_DIR)