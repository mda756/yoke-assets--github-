import asyncio
from playwright.async_api import async_playwright
import os
import json

async def main():
    print("="*70)
    print("MIRO UPLOAD - PROPER POPUP DISMISSAL")
    print("="*70)

    screenshot_name = "nexgenhc_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)
    auth_file = "miro_auth_state.json"

    if not os.path.exists(screenshot_name):
        print(f"ERROR: Screenshot not found")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)

        with open(auth_file, 'r') as f:
            storage_state = json.load(f)

        context = await browser.new_context(storage_state=storage_state)
        page = await context.new_page()
        page.set_default_timeout(120000)

        # Go to dashboard and create board
        print("\nCreating board...")
        await page.goto('https://miro.com/app/dashboard/')
        await page.wait_for_timeout(4000)

        await page.click('button:has-text("Create new"), button:has-text("Create")')
        await page.wait_for_timeout(3000)

        await page.click('text="Blank board"')
        await page.wait_for_timeout(8000)

        await page.wait_for_url('**/app/board/**', timeout=20000)
        board_url = page.url
        print(f"Board created: {board_url}")

        await page.wait_for_timeout(3000)

        # Close the "Hey matt" popup - click X button
        print("\nClosing popup...")
        try:
            # Look for X button near the popup
            await page.click('button:has-text("×")', timeout=3000)
            print("  Closed via × button")
        except:
            try:
                # Try clicking outside the popup
                await page.click('.rtb-canvas, [data-testid="board-canvas"]', position={'x': 100, 'y': 400}, timeout=3000)
                print("  Clicked outside popup")
            except:
                print("  Could not close popup")

        await page.wait_for_timeout(2000)

        # Click the + button in the LEFT TOOLBAR
        print("\nClicking + button in toolbar...")
        try:
            # Find the + button in the left toolbar
            plus_button = await page.query_selector('button:has-text("+")')
            if plus_button:
                await plus_button.click()
                print("  Clicked + button")
            else:
                await page.keyboard.press('+')
                print("  Pressed + key")
        except:
            await page.keyboard.press('+')
            print("  Pressed + key as fallback")

        await page.wait_for_timeout(2000)

        # Look for Image option in the menu
        print("\nLooking for Image option...")
        try:
            await page.click('text="Image"', timeout=5000)
            print("  Clicked Image")
        except:
            print("  Image not found")

        await page.wait_for_timeout(2000)

        # Look for file inputs
        file_inputs = await page.query_selector_all('input[type="file"]')
        print(f"\nFile inputs found: {len(file_inputs)}")

        if file_inputs:
            print("Uploading file...")
            await file_inputs[-1].set_input_files(screenshot_path)
            print("File uploaded!")
            await page.wait_for_timeout(15000)

            print("\n" + "="*70)
            print("SUCCESS!")
            print("="*70)
            print(f"Board URL: {board_url}")

        else:
            print("\nStill no file input. Taking debug screenshot...")
            await page.screenshot(path='miro_debug2.png')
            print("Debug saved: miro_debug2.png")

        print("\nBrowser staying open for 45 seconds...")
        await page.wait_for_timeout(45000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
