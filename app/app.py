import streamlit as st
import subprocess
import sys
import os

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "dummy_value_for_baml_init"

@st.cache_resource
def install_playwright_browser():
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("Playwright browser installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Playwright browser: {e}")

install_playwright_browser()


main_interface_page = st.Page(str("main_interface.py"), title="Main interface", icon=":material/add_circle:")
settings_page = st.Page(str("settings.py"), title="Settings", icon=":material/settings:")

pg = st.navigation([main_interface_page, settings_page])
st.set_page_config(page_title="Citation Generator", page_icon="📚")
pg.run()