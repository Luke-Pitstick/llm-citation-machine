from trafilatura import fetch_url, html2txt, extract
from playwright.sync_api import sync_playwright


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
        

url = "https://onlinelibrary.wiley.com/doi/full/10.1155/2021/8812542"

page = get_page(url)
extracted_text = extract(page)

print(extracted_text)