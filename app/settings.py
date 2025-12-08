import streamlit as st
from baml_py import ClientRegistry
from baml_client import b


st.title("Settings")
st.write("All settings are saved in the browser's local storage.")
st.divider()

gemini_key = st.text_input("Gemini API Key", type="password", value=st.session_state.get("gemini_key", ""))


if st.button("Save"):
    st.session_state["gemini_key"] = gemini_key
    st.success("Settings saved")
    st.rerun()

        

