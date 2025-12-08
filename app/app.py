import streamlit as st
import subprocess

subprocess.run(["playwright", "install"])
subprocess.run(["playwright", "install-deps"])

main_interface_page = st.Page(str("main_interface.py"), title="Main interface", icon=":material/add_circle:")
settings_page = st.Page(str("settings.py"), title="Settings", icon=":material/settings:")

pg = st.navigation([main_interface_page, settings_page])
st.set_page_config(page_title="Citation Generator", page_icon="📚")
pg.run()