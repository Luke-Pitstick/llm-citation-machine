import streamlit as st
from citation import generate_citations

st.set_page_config(page_title="Citation Generator", page_icon="📚")

st.title("Citation Generator")
st.write("Generate accurate MLA and APA citations from any website URL using AI.")

# Create a clean layout with columns
col1, col2 = st.columns([3, 1])

with col1:
    urls = st.text_area("Website URLs", placeholder="https://example.com").split("\n")
    for url in urls:
        if url == "":
            urls.remove(url)

with col2:
    citation_style = st.selectbox("Style", ["MLA", "APA"])
    
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
