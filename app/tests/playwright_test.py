from playwright.async_api import async_playwright
from trafilatura import html2txt
import asyncio
import random
from camoufox import Camoufox


# Realistic human interaction delays
async def human_delay(min_ms=100, max_ms=500):
    await asyncio.sleep(random.uniform(min_ms/1000, max_ms/1000))

async def get_page(url: str) -> str:
    async with Stealth().use_async(async_playwright()) as p:
        # Launch with privacy-preserving arguments
        browser = await p.chromium.launch(
            headless=False,  # Headed mode reduces detection
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True,
            java_script_enabled=True
        )
        
        # Block tracking resources but allow functional ones
        await context.route("**/*.{png,jpg,gif,svg,woff2}", lambda route: route.abort())
        
        page = await context.new_page()
        
        # Execute stealth patches directly
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            window.chrome = {runtime: {}};
        """)
        
        # Navigate with human-like pattern
        await page.goto(url, wait_until='commit')
        await human_delay(500, 1500)  # Wait before interaction
        
        # Simulate human scrolling
        for _ in range(3):
            await page.mouse.wheel(0, random.randint(200, 600))
            await human_delay(300, 800)
        
        # Wait for Cloudflare challenge resolution
        await page.wait_for_timeout(5000)
        
        content = await page.content()
        await browser.close()
        return content
    


def camoufox_scrape(url: str):
    with Camoufox(headless=True) as browser:
        page = browser.new_page()
        
        # Camoufox automatically handles Turnstile challenges
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(5000)  # Allow challenge resolution
        
        content = page.content()
        return content




url = "https://www.sciencedirect.com/science/article/abs/pii/S2468312422000104?via=ihub"

page = camoufox_scrape(url)
print("page:")
print(html2txt(page))