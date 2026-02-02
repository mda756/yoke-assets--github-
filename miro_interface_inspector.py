import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    print("Miro Interface Inspector")
    print("="*70)

    # Load credentials
    with open('claude code creator/CREDENTIALS_STORE.json', 'r') as f:
        creds = json.load(f)

    miro_email = creds['services']['miro']['email']
    miro_password = creds['services']['miro']['password']

    async with async_playwright() as p:
        # Launch browser
        print("\nLaunching browser...")
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(60000)

        # Login to Miro
        print("Logging into Miro...")
        await page.goto('https://miro.com/login/')
        await page.wait_for_timeout(2000)

        await page.fill('input[name="email"], input[type="email"]', miro_email)
        await page.fill('input[name="password"], input[type="password"]', miro_password)
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(5000)

        # Take screenshot of dashboard
        print("Capturing dashboard...")
        await page.screenshot(path='miro_dashboard.png', full_page=True)
        print("Saved: miro_dashboard.png")

        # Get HTML of dashboard
        html = await page.content()
        with open('miro_dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Saved: miro_dashboard.html")

        # Try to create board
        print("\nAttempting to create board...")

        # Method 1: Look for any buttons with "create" text
        all_buttons = await page.query_selector_all('button, a')
        print(f"Found {len(all_buttons)} buttons/links")

        for button in all_buttons[:20]:  # Check first 20
            try:
                text = await button.text_content()
                if text and ('create' in text.lower() or 'new' in text.lower() or 'board' in text.lower()):
                    print(f"  Found button: {text[:50]}")
            except:
                pass

        # Try clicking create board
        try:
            # Wait a bit longer for dashboard to load
            await page.wait_for_timeout(3000)

            # Try multiple methods
            await page.click('button:has-text("Create")', timeout=5000)
            print("Clicked Create button")
        except:
            try:
                await page.click('text="Create new board"', timeout=5000)
                print("Clicked Create new board")
            except:
                try:
                    # Try using + button or similar
                    await page.click('[aria-label*="Create"]', timeout=5000)
                    print("Clicked Create via aria-label")
                except:
                    print("Could not find create button, trying keyboard...")
                    await page.keyboard.press('Control+N')

        await page.wait_for_timeout(5000)

        # Take screenshot after board creation attempt
        print("\nCapturing board interface...")
        await page.screenshot(path='miro_board_interface.png', full_page=True)
        print("Saved: miro_board_interface.png")

        # Get HTML of board
        html = await page.content()
        with open('miro_board_interface.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Saved: miro_board_interface.html")

        # Look for upload-related elements
        print("\nSearching for upload elements...")
        file_inputs = await page.query_selector_all('input[type="file"]')
        print(f"File inputs found: {len(file_inputs)}")

        upload_buttons = await page.query_selector_all('button:has-text("Upload"), [aria-label*="upload" i]')
        print(f"Upload buttons found: {len(upload_buttons)}")

        # Get current URL
        current_url = page.url
        print(f"\nCurrent URL: {current_url}")

        print("\n" + "="*70)
        print("Inspection complete! Check the generated files:")
        print("  - miro_dashboard.png")
        print("  - miro_dashboard.html")
        print("  - miro_board_interface.png")
        print("  - miro_board_interface.html")
        print("\nBrowser staying open for 30 seconds for manual inspection...")
        await page.wait_for_timeout(30000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
