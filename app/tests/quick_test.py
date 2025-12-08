from trafilatura import fetch_url, html2txt, extract
from playwright.sync_api import sync_playwright
import requests


def get_page(url: str):
    """
    Fetches page content. 
    Note: For production, consider passing a single browser instance 
    into this function rather than launching a new one every time.
    """
    with sync_playwright() as p:
        # headless=True is faster, but False is better for debugging bot detection
        browser = p.chromium.launch(headless=True) 
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080} # Explicit viewport helps with rendering
        )
        
        try:
            page = context.new_page()
            
            # "domcontentloaded" is fast, but "networkidle" is safer for extracting dynamic text
            page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Fallback: simple wait to ensure JS renders text
            page.wait_for_timeout(1000) 

            content = page.content()
            return content
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""
        finally:
            browser.close()
        
def get_page_with_requests(url: str):
    response = requests.get(url)
    return response.text

url = "https://www.sciencedirect.com/science/article/abs/pii/S2468312422000104?via=ihub"

page = get_page(url)
print("page:")
print(html2txt(page))
# print("page with playwright:")
# page_with_playwright = html2txt(get_page_with_playwright(url))
# print(page_with_playwright)