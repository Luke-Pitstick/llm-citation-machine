import streamlit as st
from citation import generate_mla_citation, generate_apa_citation

st.set_page_config(page_title="Citation Generator", page_icon="📚")

st.title("Citation Generator")
st.write("Generate accurate MLA and APA citations from any website URL using AI.")

# Create a clean layout with columns
col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input("Website URL", placeholder="https://example.com")

with col2:
    citation_style = st.selectbox("Style", ["MLA", "APA"])

if st.button("Generate Citation", type="primary"):
    if not url:
        st.error("Please enter a URL first.")
    else:
        with st.spinner("Generating citation..."):
            try:
                # Call the citation function
                if citation_style == "MLA":
                    citation, info = generate_mla_citation(url)
                elif citation_style == "APA":
                    citation, info = generate_apa_citation(url)
                
                # Display the result
                st.success("Citation generated!")
                
                st.subheader("Citation")
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
