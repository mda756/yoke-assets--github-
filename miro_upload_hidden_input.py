import asyncio
from playwright.async_api import async_playwright
import os
import json

async def main():
    print("="*70)
    print("MIRO UPLOAD - HIDDEN FILE INPUT METHOD")
    print("="*70)

    screenshot_name = "nexgenhc_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)
    auth_file = "miro_auth_state.json"

    # Make sure screenshot exists
    if not os.path.exists(screenshot_name):
        print(f"ERROR: Screenshot not found: {screenshot_name}")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=300)

        with open(auth_file, 'r') as f:
            storage_state = json.load(f)

        context = await browser.new_context(storage_state=storage_state)
        page = await context.new_page()
        page.set_default_timeout(120000)

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

        await page.wait_for_timeout(2000)

        # Dismiss popups
        print("Dismissing popups...")
        try:
            await page.click('button[aria-label="Close"]', timeout=2000)
            print("  Closed popup")
        except:
            pass

        await page.wait_for_timeout(1000)

        # Try clicking + menu
        print("\nOpening + menu...")
        await page.keyboard.press('+')
        await page.wait_for_timeout(2000)

        # Click Image
        print("Clicking Image...")
        try:
            await page.click('button:has-text("Image"), text="Image"', timeout=3000)
        except:
            print("  Could not find Image button")

        await page.wait_for_timeout(2000)

        # Look for ANY file input (hidden or visible)
        print("\nSearching for file input elements...")
        file_inputs = await page.query_selector_all('input[type="file"]')
        print(f"Found {len(file_inputs)} file input(s)")

        if file_inputs:
            # Use the last one (most recently created)
            print(f"Using file input to upload...")
            await file_inputs[-1].set_input_files(screenshot_path)
            print("File set on input element!")

            # Wait for upload
            await page.wait_for_timeout(15000)

            print("\n" + "="*70)
            print("UPLOAD COMPLETE")
            print("="*70)
            print(f"\nBoard URL: {board_url}")

        else:
            print("\nNo file input found. Taking screenshot for debugging...")
            await page.screenshot(path='miro_debug.png')
            print("Debug screenshot saved: miro_debug.png")

        print("\nBrowser staying open for 30 seconds...")
        await page.wait_for_timeout(30000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
