import asyncio
from playwright.async_api import async_playwright
import sys

async def scroll_to_bottom(page):
    """Scroll to bottom to trigger lazy loading"""
    page_height = await page.evaluate('document.body.scrollHeight')
    viewport_height = await page.evaluate('window.innerHeight')
    current_position = 0
    scroll_step = viewport_height

    while current_position < page_height:
        await page.evaluate(f'window.scrollTo(0, {current_position})')
        await page.wait_for_timeout(500)
        current_position += scroll_step
        new_height = await page.evaluate('document.body.scrollHeight')
        if new_height > page_height:
            page_height = new_height

    await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    await page.wait_for_timeout(1000)
    await page.evaluate('window.scrollTo(0, 0)')
    await page.wait_for_timeout(500)

async def main():
    if len(sys.argv) < 2:
        print("Usage: python capture_website_screenshot.py <URL> [output_filename]")
        print("Example: python capture_website_screenshot.py https://example.com example_screenshot.png")
        return

    url = sys.argv[1]

    # Generate filename from URL if not provided
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        # Extract domain from URL for filename
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.replace('www.', '').replace('.', '_')
        output_file = f"{domain}_homepage.png"

    print("="*70)
    print("WEBSITE SCREENSHOT CAPTURE")
    print("="*70)
    print(f"\nURL: {url}")
    print(f"Output: {output_file}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(90000)

        print("\nNavigating to website...")
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(3000)

        print("Scrolling to load all content (lazy loading)...")
        await scroll_to_bottom(page)

        print("Capturing full-page screenshot...")
        await page.screenshot(path=output_file, full_page=True)

        await browser.close()

        print("\n" + "="*70)
        print("SCREENSHOT SAVED!")
        print("="*70)
        print(f"\nFile: {output_file}")
        print("Ready to upload to Miro manually")

if __name__ == "__main__":
    asyncio.run(main())
