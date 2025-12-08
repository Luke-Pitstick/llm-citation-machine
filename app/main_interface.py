import streamlit as st
from src.citation import generate_citations
from baml_py import ClientRegistry
from baml_client import b


def create_gemini_client():
    try: 
        gemini_key = st.session_state["gemini_key"]
    except KeyError:
        st.error("Gemini API key not found. Please set it in the settings.")
        st.stop()


    try:
        b.client_registry.add_llm_client(
            name='CustomGemini',
            provider='google-ai',
            options={
                "model": "gemini-2.5-flash",
                "api_key": gemini_key
            }
        )
        b.client_registry.set_primary('CustomGemini')
    except Exception as e:
        # Fallback if accessing client_registry directly fails in your specific version
        print(f"Could not update registry directly: {e}")
    

st.set_page_config(page_title="Citation Generator", page_icon="📚")


st.title("Citation Generator")
st.write("Generate accurate MLA and APA citations from any article URL using AI.")

st.divider()

# Create a clean layout with columns
col1, col2 = st.columns([3, 1])

with col1:
    urls = st.text_area("Website URLs", placeholder="https://example.com").split("\n")
    for url in urls:
        if url == "":
            urls.remove(url)

with col2:
    citation_style = st.selectbox("Style", ["MLA", "APA"])
    
create_gemini_client()

    
if st.button("Generate Citation", type="primary"):

    if not urls:
        st.error("Please enter some URLs first.")
    else:
        with st.spinner("Generating citations..."):
            try:
                # Call the citation function
                citations, info_list = generate_citations(urls, citation_style)
                
                
                # Display the result
                st.success(f"{len(citations)} citations generated!")
                
                for i, (citation, info) in enumerate(zip(citations, info_list)):
                    st.subheader(f"Citation {i+1}")
                # Display rendered markdown for visual check
                    st.markdown(citation)
                    
                    # specific copy block
                    st.caption("Copy raw markdown:")
                    st.code(citation, language="markdown")
                    
                    # Show metadata in an expandable section
                    with st.expander("View Extracted Metadata"):
                        st.json(info.model_dump())
            except Exception as e:
                st.error(f"Error: {str(e)}")
