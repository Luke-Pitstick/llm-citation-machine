import json
import datetime
from dotenv import load_dotenv


from trafilatura import fetch_url, extract, html2txt
from playwright.sync_api import sync_playwright


from baml_client.types import Website, Date, CitationInfo, Author
from baml_client import b

# Rebuild models to resolve forward references (Date is defined after CitationInfo alphabetically)
CitationInfo.model_rebuild()

load_dotenv()


def get_page(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=False helps pass bot checks
        context = browser.new_context(  # this enables cookies & JS automatically
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Load page (don’t block early)
        page.goto(url, wait_until="domcontentloaded")

        content = page.content()
        browser.close()
        return content


def split_text(text: str, max_length: int = 10000):
    """
    Split text into chunks of a given length. This is used to avoid giving the LLM to many tokens which helps to optimize costs and speed.
    """
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]




def extract_citation_info(cite_url, date_accessed: datetime.date):
    """
    Extract citation info from a website. Uses
    """
    
    text = get_page(cite_url)
    text = html2txt(text)
    text = split_text(text, 6000)[0]
    
    if text is None:
        raise ValueError(f"Failed to extract content from {cite_url}")
    
    website = Website(url=cite_url, content=text)
    access_date = Date(day=str(date_accessed.day), month=str(date_accessed.month), year=str(date_accessed.year))
    
    return b.ExtractCitationInfo(website=website, access_date=access_date)


def generate_mla_citation(url: str):
    info = extract_citation_info(url, datetime.date.today())
    print(info)
    
    citation = ""    
    for i in range(len(info.authors)):
        name = ""
        author = info.authors[i]
        name += author.last_name + ", "
        
        for first_name in author.first_name.split(" "):
            name += first_name + " "
        name = name.strip()
            
        
        citation += name + ", "
        
        if len(info.authors) >= 3:
            citation += "et al."
            break
        

    citation += ' "' + info.article_title + '."'
    citation += " *"
    citation += info.website_title + "*" +","
    
    if info.volume:
        citation += " vol. " + info.volume + ","
        
    if info.issue:
        citation += " no. " + info.issue + ","
        
    citation += " " + info.publication_date.year + ","
    
    if info.page_range:
        citation += " pp. " + info.page_range + ","
    
    
    if info.doi:
        citation += " doi:https://doi.org/" + info.doi + "."
    return citation, info
    

def generate_apa_citation(url: str):
    info = extract_citation_info(url, datetime.date.today())
    print(info)
    
    citation = ""
    for i in range(len(info.authors)):
        name = ""
        author = info.authors[i]
        name += author.last_name + ", "
        for first_name in author.first_name.split(" "):
            name += first_name + " "
        name = name.strip()
        citation += name + ", "
        
        if len(info.authors) >= 3:
            citation += "et al."
            break

    citation += ' "' + info.article_title + '."'
    citation += " *"
    citation += info.website_title + "*" +","
    
    if info.volume:
        citation += " vol. " + info.volume + ","
        

    if info.issue:
        citation += " no. " + info.issue + ","
        
    citation += " " + info.publication_date.year + ","
    
    if info.page_range:
        citation += " pp. " + info.page_range + ","

    if info.doi:
        citation += " doi:https://doi.org/" + info.doi + "."
    return citation, info

if __name__ == "__main__":
    test_url = "https://onlinelibrary.wiley.com/doi/full/10.1002/fsn3.362"
    correct_citation = "Mishfa KF, Alim MA, Repon MR, et al. Preparation and characterization of snake plant fiber reinforced composite: A sustainable utilization of biowaste. SPE Polym. 2024; 5(1): 35-44. doi:10.1002/pls2.10108"
    citation, _ = generate_mla_citation(test_url)
    print("\n\nCorrect Citation:")
    print(citation)