import asyncio
from playwright.async_api import async_playwright
import os
import json

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
    print("="*70)
    print("MIRO UPLOAD - DIRECT FILE INPUT METHOD")
    print("="*70)

    screenshot_name = "nexgenhc_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)
    auth_file = "miro_auth_state.json"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=300)

        with open(auth_file, 'r') as f:
            storage_state = json.load(f)

        context = await browser.new_context(storage_state=storage_state)
        page = await context.new_page()
        page.set_default_timeout(120000)

        # Capture screenshot if needed
        if not os.path.exists(screenshot_name):
            print("\nCapturing nexgenhc.com...")
            await page.goto('https://nexgenhc.com/', wait_until="networkidle")
            await page.wait_for_timeout(3000)
            await scroll_to_bottom(page)
            await page.screenshot(path=screenshot_name, full_page=True)
            print(f"Screenshot saved: {screenshot_name}")

        # Go to Miro dashboard
        print("\nGoing to Miro dashboard...")
        await page.goto('https://miro.com/app/dashboard/')
        await page.wait_for_timeout(4000)

        # Create new board
        print("Creating new board...")
        await page.click('button:has-text("Create new"), button:has-text("Create")')
        await page.wait_for_timeout(3000)

        await page.click('text="Blank board"')
        await page.wait_for_timeout(8000)

        await page.wait_for_url('**/app/board/**', timeout=20000)
        board_url = page.url
        print(f"Board created: {board_url}")

        # Name board
        print("Naming board...")
        await page.wait_for_timeout(2000)

        # Click on title and rename
        try:
            await page.click('text="Untitled"', timeout=5000)
            await page.wait_for_timeout(500)
            await page.keyboard.press('Control+A')
            await page.keyboard.type("nexgenhc home screen")
            await page.keyboard.press('Enter')
            print("Board named: nexgenhc home screen")
        except:
            print("Could not rename board")

        await page.wait_for_timeout(2000)

        # Dismiss any Miro AI popups or overlays
        print("Dismissing popups...")
        popup_close_selectors = [
            'button[aria-label="Close"]',
            'button:has-text("Close")',
            '[data-testid="modal-close"]',
            'button:has-text("×")',
            '.close-button',
            '[aria-label*="close" i]'
        ]

        for selector in popup_close_selectors:
            try:
                await page.click(selector, timeout=2000)
                print(f"  Closed popup: {selector}")
                await page.wait_for_timeout(500)
            except:
                continue

        # Click on board canvas to ensure no popups blocking
        try:
            await page.click('[data-testid="board-canvas"], .rtb-canvas, body', timeout=3000)
            print("  Board canvas focused")
        except:
            pass

        await page.wait_for_timeout(1000)

        # Upload using file chooser interception
        print("\nUploading screenshot using file chooser...")

        # Set up file chooser handler BEFORE triggering it
        async with page.expect_file_chooser() as fc_info:
            # Press + to open toolbar menu
            await page.keyboard.press('+')
            await page.wait_for_timeout(1500)

            # Click Image button to trigger file chooser
            try:
                await page.click('button:has-text("Image"), [aria-label*="Image" i]', timeout=5000)
                print("  Clicked Image button")
            except:
                # Try alternative selector
                await page.click('text="Image"', timeout=5000)
                print("  Clicked Image text")

        file_chooser = await fc_info.value
        await file_chooser.set_files(screenshot_path)
        print(f"File uploaded via chooser: {screenshot_name}")

        # Wait for upload to process
        await page.wait_for_timeout(10000)

        print("\n" + "="*70)
        print("UPLOAD COMPLETE")
        print("="*70)
        print(f"\nBoard: nexgenhc home screen")
        print(f"URL: {board_url}")

        # Take verification screenshot
        await page.screenshot(path='board_final_verification.png')
        print("\nVerification screenshot saved: board_final_verification.png")

        print("\nBrowser staying open for 30 seconds...")
        await page.wait_for_timeout(30000)

        await browser.close()

        # Clean up
        if os.path.exists(screenshot_name):
            os.remove(screenshot_name)
            print(f"\nCleaned up: {screenshot_name}")

if __name__ == "__main__":
    asyncio.run(main())
