
import asyncio
from playwright.async_api import async_playwright

async def screenshot():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1024, "height": 768})
        
        # Screenshot 1: Login
        await page.goto("http://localhost:5000/login", wait_until="networkidle")
        await page.screenshot(path="login.png")
        print("✓ Screenshot 1: Login")
        
        # Screenshot 2: Dashboard (depois de login)
        await page.fill('input[name="email"]', 'admin@osgade.local')
        await page.fill('input[name="senha"]', 'admin123')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path="dashboard.png")
        print("✓ Screenshot 2: Dashboard")
        
        # Screenshot 3: Lista de crianças
        await page.goto("http://localhost:5000/criancas", wait_until="networkidle")
        await page.screenshot(path="criancas.png")
        print("✓ Screenshot 3: Lista de crianças")
        
        await browser.close()

asyncio.run(screenshot())
