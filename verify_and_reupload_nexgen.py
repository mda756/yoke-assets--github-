import asyncio
from playwright.async_api import async_playwright
import pyautogui
import time
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
    print("VERIFY AND RE-UPLOAD NEXGENHC TO MIRO")
    print("="*70)

    # Re-capture the screenshot first
    screenshot_name = "nexgenhc_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)
    auth_file = "miro_auth_state.json"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)

        # Load saved authentication
        with open(auth_file, 'r') as f:
            storage_state = json.load(f)

        context = await browser.new_context(storage_state=storage_state)
        page = await context.new_page()
        page.set_default_timeout(120000)

        # Capture nexgenhc.com if not exists
        if not os.path.exists(screenshot_name):
            print("\nCapturing nexgenhc.com screenshot...")
            await page.goto('https://nexgenhc.com/', wait_until="networkidle")
            await page.wait_for_timeout(3000)
            await scroll_to_bottom(page)
            await page.screenshot(path=screenshot_name, full_page=True)
            print(f"Screenshot captured: {screenshot_name}")
        else:
            print(f"\nScreenshot exists: {screenshot_name}")

        # Open the board
        board_url = "https://miro.com/app/board/uXjVGI56yUs=/"
        print(f"\nOpening Miro board: {board_url}")
        await page.goto(board_url)
        await page.wait_for_timeout(5000)

        print("Board opened. Preparing to upload...")

        # Focus the board
        await page.bring_to_front()
        await page.wait_for_timeout(1000)

        # Click on board canvas to ensure focus
        try:
            canvas = await page.wait_for_selector('[data-testid="board-canvas"], .rtb-canvas', timeout=5000)
            await canvas.click()
            print("Board canvas focused")
        except:
            await page.click('body')
            print("Board focused via body click")

        await page.wait_for_timeout(1000)

        # Try multiple upload methods
        print("\nAttempting upload method 1: Ctrl+U...")
        await page.keyboard.press('Control+U')
        await page.wait_for_timeout(3000)

        # Check if file dialog opened by looking for file input
        file_inputs = await page.query_selector_all('input[type="file"]')

        if not file_inputs:
            print("Method 1 failed. Trying method 2: + menu...")
            await page.keyboard.press('+')
            await page.wait_for_timeout(2000)

            # Try clicking Image button
            try:
                await page.click('button:has-text("Image"), text="Image"', timeout=3000)
                await page.wait_for_timeout(2000)
            except:
                print("Could not find Image button")

        # Now use OS automation to handle file dialog
        print("\nUsing OS automation to select file...")
        print(f"File path: {screenshot_path}")

        time.sleep(2)

        # Type the full path
        pyautogui.write(screenshot_path, interval=0.05)
        time.sleep(1)

        # Press Enter to select
        pyautogui.press('enter')
        print("File selection sent")

        # Wait longer for upload to complete
        print("\nWaiting for upload to complete...")
        await page.wait_for_timeout(15000)

        # Verify upload by checking if there are images on the board
        print("\nVerifying upload...")
        try:
            images = await page.query_selector_all('img[src*="miro"], [data-testid*="image"]')
            if images and len(images) > 0:
                print(f"VERIFICATION SUCCESS: Found {len(images)} image(s) on board")
            else:
                print("WARNING: No images detected on board")
                print("The upload may have failed. Please check the board manually.")
        except Exception as e:
            print(f"Verification check: {str(e)[:100]}")

        # Take a screenshot of the board for verification
        print("\nTaking screenshot of board for verification...")
        await page.screenshot(path='miro_board_verification.png', full_page=False)
        print("Board screenshot saved: miro_board_verification.png")

        print("\n" + "="*70)
        print("UPLOAD ATTEMPT COMPLETE")
        print("="*70)
        print(f"\nBoard URL: {board_url}")
        print(f"Screenshot file: {screenshot_name}")
        print("\nPlease check:")
        print("1. The Miro board in the browser window")
        print("2. The verification screenshot: miro_board_verification.png")

        print("\nBrowser staying open for 60 seconds for manual verification...")
        await page.wait_for_timeout(60000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
