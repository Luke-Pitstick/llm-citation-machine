import os
import sys
from pathlib import Path
import requests

def install_browserforge():
    # Set custom data directory in a writable location
    DATA_DIR = Path("/tmp/browserforge_data")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Set environment variable before importing browserforge
    os.environ["BROWSERFORGE_DATA_DIR"] = str(DATA_DIR)

    # Download model files manually
    files = {
        "fingerprint-network.zip": "https://github.com/daijro/browserforge/releases/download/v1.0.0/fingerprint-network.zip",
        "input-network.zip": "https://github.com/daijro/browserforge/releases/download/v1.0.0/input-network.zip"
    }

    for filename, url in files.items():
        filepath = DATA_DIR / filename
        if not filepath.exists():
            print(f"Downloading {filename}...")
            response = requests.get(url)
            response.raise_for_status()
            filepath.write_bytes(response.content)
            print(f"Saved to {filepath}")
        else:
            print(f"{filename} already exists at {filepath}")

    print(f"BrowserForge data directory set to: {DATA_DIR}")
    print(f"Files downloaded: {list(DATA_DIR.glob('*.zip'))}")