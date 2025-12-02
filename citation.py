import json
import datetime

from trafilatura import fetch_url, extract, html2txt

from baml_client.types import Website, Date
from baml_client import b




def extract_citation_info(cite_url, date_accessed: datetime.date):
    """
    Extract citation info from a website.
    """
    
    text = extract(fetch_url(cite_url))
    
    if text is None:
        raise ValueError(f"Failed to extract content from {cite_url}")
    
    website = Website(url=cite_url, content=text)
    access_date = Date(day=date_accessed.day, month=date_accessed.month, year=date_accessed.year)
    
    return b.ExtractCitationInfo(website=website, access_date=access_date)


if __name__ == "__main__":
    test_url = "https://ashpublications.org/blood/article/112/13/4793/24896/Stem-cell-concepts-renew-cancer-research"
    info = extract_citation_info(test_url, datetime.date.today())
    info_dict = info.model_dump()
    print(info_dict)
    