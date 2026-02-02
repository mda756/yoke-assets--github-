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
    print("NEXGENHC.COM TO MIRO - FULLY AUTOMATIC")
    print("="*70)

    screenshot_name = "nexgenhc_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)
    auth_file = "miro_auth_state.json"

    if not os.path.exists(auth_file):
        print(f"\nERROR: Authentication file not found: {auth_file}")
        print("Please run miro_save_session.py first to save your login.")
        return

    print("\nUsing saved Miro authentication...")

    async with async_playwright() as p:
        print("\n1. CAPTURING NEXGENHC.COM SCREENSHOT")
        print("="*70)

        browser = await p.chromium.launch(headless=False, slow_mo=500)

        # Load saved authentication state
        with open(auth_file, 'r') as f:
            storage_state = json.load(f)

        context = await browser.new_context(storage_state=storage_state)
        page = await context.new_page()
        page.set_default_timeout(120000)

        # Capture nexgenhc.com
        print("\nNavigating to nexgenhc.com...")
        await page.goto('https://nexgenhc.com/', wait_until="networkidle")
        await page.wait_for_timeout(3000)

        print("Scrolling to load all content...")
        await scroll_to_bottom(page)

        print("Taking full-page screenshot...")
        await page.screenshot(path=screenshot_name, full_page=True)
        print(f"Screenshot saved: {screenshot_name}")

        # Now go to Miro
        print("\n2. CREATING MIRO BOARD")
        print("="*70)

        print("\nNavigating to Miro dashboard...")
        await page.goto('https://miro.com/app/dashboard/')
        await page.wait_for_timeout(4000)

        print("Already logged in via saved session!")

        # Create board
        print("\nCreating new board...")
        await page.click('button:has-text("Create new"), button:has-text("Create")')
        await page.wait_for_timeout(3000)

        await page.click('text="Blank board"')
        await page.wait_for_timeout(8000)

        await page.wait_for_url('**/app/board/**', timeout=20000)
        board_url = page.url
        print(f"Board created: {board_url}")

        # Name board
        print("\nNaming board...")
        board_name = "nexgenhc home screen"
        await page.wait_for_timeout(2000)

        await page.evaluate(f'''
            const titleInputs = document.querySelectorAll('input[placeholder*="Untitled"], input[placeholder*="title"]');
            for (const el of titleInputs) {{
                el.value = "{board_name}";
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        ''')
        print(f"Board named: {board_name}")
        await page.wait_for_timeout(2000)

        # Upload screenshot
        print("\n3. UPLOADING SCREENSHOT")
        print("="*70)

        await page.bring_to_front()
        await page.wait_for_timeout(1000)
        await page.click('body')
        await page.wait_for_timeout(500)

        await page.keyboard.press('Control+U')
        await page.wait_for_timeout(2000)

        print("\nUsing OS automation to select file...")
        time.sleep(2)
        pyautogui.write(screenshot_path, interval=0.05)
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(3)

        print("Screenshot uploaded!")
        await page.wait_for_timeout(8000)

        print("\n" + "="*70)
        print("SUCCESS!")
        print("="*70)
        print(f"\nBoard: {board_name}")
        print(f"URL: {board_url}")
        print("Screenshot: nexgenhc.com homepage")

        print("\nBrowser staying open for 30 seconds...")
        await page.wait_for_timeout(30000)
        await browser.close()

        # Clean up
        if os.path.exists(screenshot_name):
            os.remove(screenshot_name)
            print(f"\nCleaned up: {screenshot_name}")

if __name__ == "__main__":
    asyncio.run(main())
