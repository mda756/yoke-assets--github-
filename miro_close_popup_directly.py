import asyncio
from playwright.async_api import async_playwright
import os
import json

async def main():
    print("="*70)
    print("MIRO - CLOSE POPUP AND UPLOAD")
    print("="*70)

    screenshot_name = "nexgenhc_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)
    auth_file = "miro_auth_state.json"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=800)

        with open(auth_file, 'r') as f:
            storage_state = json.load(f)

        context = await browser.new_context(storage_state=storage_state)
        page = await context.new_page()
        page.set_default_timeout(120000)

        # Create board
        print("\nCreating board...")
        await page.goto('https://miro.com/app/dashboard/')
        await page.wait_for_timeout(4000)

        await page.click('button:has-text("Create new")')
        await page.wait_for_timeout(3000)

        await page.click('text="Blank board"')
        await page.wait_for_timeout(8000)

        await page.wait_for_url('**/app/board/**', timeout=20000)
        board_url = page.url
        print(f"Board: {board_url}")

        await page.wait_for_timeout(3000)

        # Find and close the popup by clicking X at specific coordinates
        print("\nClosing popup at specific location...")
        # The X button is at approximately (987, 191) based on the screenshot
        try:
            await page.mouse.click(987, 191)
            print("  Clicked X button at coordinates")
        except:
            print("  Click failed, trying selector")

        await page.wait_for_timeout(2000)

        # Verify popup is closed
        await page.screenshot(path='after_close_popup.png')
        print("Screenshot after closing popup: after_close_popup.png")

        # Now try to upload
        print("\nAttempting upload...")

        # Look for the image icon in the left toolbar (looks like a picture frame icon)
        # It should be around the 3rd or 4th icon down
        toolbar_icons = [
            '[aria-label*="Image" i]',
            'button[title*="Image" i]',
            '[data-testid*="image" i]'
        ]

        for selector in toolbar_icons:
            try:
                await page.click(selector, timeout=2000)
                print(f"  Clicked: {selector}")
                break
            except:
                continue

        await page.wait_for_timeout(2000)

        # Look for file input
        file_inputs = await page.query_selector_all('input[type="file"]')
        print(f"File inputs: {len(file_inputs)}")

        if file_inputs:
            await file_inputs[-1].set_input_files(screenshot_path)
            print("UPLOADED!")
            await page.wait_for_timeout(15000)

            print("\n" + "="*70)
            print("SUCCESS!")
            print("="*70)
            print(f"Board: {board_url}")
        else:
            print("No file input found yet")

        await page.screenshot(path='final_result.png')
        print("\nFinal: final_result.png")

        print("\nBrowser open for 60 seconds...")
        await page.wait_for_timeout(60000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
