import datetime

from trafilatura import html2txt

from src.baml_client.types import Website, Date, CitationInfo
from src.baml_client import b
from baml_py import ClientRegistry
import requests

CitationInfo.model_rebuild()

api_url = "https://citation-api-353156069680.us-central1.run.app"

def get_page(url: str):
    response = requests.get(f"{api_url}/extract-citation-info?url={url}")
    return response.json()["citation_info"]

def split_text(text: str, max_length: int = 10000):
    """
    Split text into chunks of a given length. This is used to avoid giving the LLM to many tokens which helps to optimize costs and speed.
    """
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]




def extract_citation_info(cite_url, date_accessed: datetime.date, registry: ClientRegistry):
    """
    Extract citation info from a website. Uses
    """
    
    text = get_page(cite_url)
    text = html2txt(text)
    #text = split_text(text, 15000)[0]
    
    if text is None:
        raise ValueError(f"Failed to extract content from {cite_url}")
    
    website = Website(url=cite_url, content=text)
    access_date = Date(day=str(date_accessed.day), month=str(date_accessed.month), year=str(date_accessed.year))
    
    return b.ExtractCitationInfo(website=website, access_date=access_date, baml_options={"client_registry": registry})

def generate_mla_citation(info: CitationInfo):
    citation = ""
    name = ""
    author = info.authors[0]
    name += f"{author.last_name}, "
    
    
    for first_name in author.first_name.split(" "):
        name += f"{first_name} "
    name = name.strip()
        
    
    citation += f"{name}"
    
    for i in range(1, len(info.authors)):
        author = info.authors[i]
        
        name = f", {author.first_name} {author.last_name}"
        
        if i < len(info.authors) - 1 and len(info.authors) == 2:
            citation += ", and "
        
        if len(info.authors) >= 3:
            citation += ", et al."
            break
        

    citation += f' "{info.article_title}."'
    citation += " *"
    citation += f"{info.publication_title}*" +","
    
    if info.volume:
        citation += f" vol. {info.volume},"
        
    if info.issue:
        citation += f" no. {info.issue},"
        
    citation += f" {info.publication_date.year},"
    
    
    citation += f" pp. {info.page_range},"

    if info.doi:
        citation += f" DOI https://doi.org/{info.doi}."
    return citation, info


def generate_apa_citation(info: CitationInfo):
    citation = ""    
    for i in range(len(info.authors)):
        if i == (len(info.authors) - 1):
            print("last author")
            citation += "& "
        
        citation += f"{info.authors[i].last_name}, "
        for first_name in info.authors[i].first_name.split(" "):
            citation += f"{first_name[0].strip()}. "
            
        citation += ", "
        
    
    citation = citation.strip()
    citation = citation[0:-2]
    citation += f" ({info.publication_date.year}). "
    citation += f"{info.article_title}. "
    citation += f"*{info.publication_title}*, "
    if info.volume:
        citation += f"*{info.volume}*"
    if info.issue:
        citation += f"({info.issue}), "
    else:
        citation += ", "
    
    if "-" not in info.page_range: 
        citation += f"Article {info.page_range}. " 
    else:
        citation += f"{info.page_range}. "
    citation += f"https://doi.org/{info.doi}"
    
    return citation, info

def generate_citations(urls: list[str], style: str, registry: ClientRegistry):
    citations = []
    info_list = []
    for url in urls:
        citation_info = extract_citation_info(url, datetime.date.today(), registry)
        if style == "MLA":
            citation, info = generate_mla_citation(citation_info)
        elif style == "APA":
            citation, info = generate_apa_citation(citation_info)
        citations.append(citation)
        info_list.append(info)
    return citations, info_list

if __name__ == "__main__":
    test_url = "https://onlinelibrary.wiley.com/doi/full/10.1002/fsn3.362"
    page = get_page(test_url)
    print(page)