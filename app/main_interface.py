import asyncio

import streamlit as st
from baml_py import ClientRegistry

from src.citation import generate_citations
from src.citation import extract_citation_info
from src.citation import generate_apa_citation, generate_mla_citation



st.set_page_config(page_title="Citation Generator", page_icon="📚")

st.title("Citation Generator")
st.write("Generate accurate MLA and APA citations from any article URL using Gemini and BAML.  \
         If the HTML can't be extracted put in any citation info you can find and it will generate the citation for you.")

st.divider()

# Create a clean layout with columns
col1, col2 = st.columns([3, 1])

with col1:
    urls = st.text_area("Website URLs", placeholder="https://example.com").split("\n")
    urls = [url.strip() for url in urls if url.strip()]

with col2:
    citation_style = st.selectbox("Style", ["MLA", "APA"])


gemini_key = st.session_state.get("gemini_key")

    
if st.button("Generate Citation", type="primary"):
    if not gemini_key:
        st.error("Please enter your Gemini API key in the settings page to generate citations.")
    elif not urls:
        st.error("Please enter some URLs first.")
    else:
        with st.spinner("Generating citations...", show_time=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            results_container = st.container()
            
            registry = ClientRegistry()
            registry.add_llm_client(
                name='CustomGemini',
                provider='google-ai',
                options={
                    "model": "gemini-2.5-flash",
                    "api_key": gemini_key
                }
            )
            
            
            async def process_urls():
                tasks = [extract_citation_info(url, citation_style, registry) for url in urls]
    
                completed_count = 0
                
                for coro in asyncio.as_completed(tasks):
                    # try:
                        citation_info = await coro
                        
                        if citation_style == "MLA":
                            citation, info = generate_mla_citation(citation_info)
                        elif citation_style == "APA":
                            citation, info = generate_apa_citation(citation_info)

                        with results_container:
                            st.subheader(f"Citation {completed_count + 1}")
                            st.markdown(citation)
                            st.caption("Copy raw markdown:")
                            st.code(citation, language="markdown")
                            with st.expander("View Extracted Metadata"):
                                st.json(info.model_dump())
                        
                            completed_count += 1
                            progress_bar.progress(completed_count / len(urls))
                            status_text.text(f"Completed {completed_count}/{len(urls)} citations")

                    # except Exception as e:
                    #     with results_container:
                    #         st.error(f"Error generating citation: {e}")
                    #         print(e)
                    #     completed_count += 1
                    #     progress_bar.progress(completed_count / len(urls))
                        
                status_text.success(f"All {len(urls)} citations generated!")
            
            
            try:
                asyncio.run(process_urls())
            except Exception as e:
                st.error(f"Error: {str(e)}")
            
            
            
            
            
            # try:    
                
            #     citations, info_list = generate_citations(urls, citation_style, registry)
                
                
            #     # Display the result
            #     st.success(f"{len(citations)} citations generated!")
                
            #     for i, (citation, info) in enumerate(zip(citations, info_list)):
            #         st.subheader(f"Citation {i+1}")
            #     # Display rendered markdown for visual check
            #         st.markdown(citation)
                    
            #         # specific copy block
            #         st.caption("Copy raw markdown:")
            #         st.code(citation, language="markdown")
                    
            #         # Show metadata in an expandable section
            #         with st.expander("View Extracted Metadata"):
            #             st.json(info.model_dump())
            # except Exception as e:
            #     st.error(f"Error: {str(e)}")
