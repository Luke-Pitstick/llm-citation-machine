from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI
from camoufox.async_api import AsyncCamoufox
from trafilatura import html2txt
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="API for LLM Citation Machine", description="API for LLM Citation Machine", version="0.1.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
@limiter.limit("10/minute")
def read_root(request: Request):
    return {"Hello": "LLM Citation Machine API"}


@app.get("/extract-citation-info")
@limiter.limit("20/minute")
async def extract_citation_info(request: Request, url: str):
    async with AsyncCamoufox(headless=True) as browser:
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(5000)
        content = await page.content()
        text = html2txt(content)
        return {"citation_info": text}

