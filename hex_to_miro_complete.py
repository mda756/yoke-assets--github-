import asyncio
from playwright.async_api import async_playwright
import pyautogui
import time
import os

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
    print("HEX.CO TO MIRO - COMPLETE WORKFLOW")
    print("="*70)

    screenshot_name = "hex_co_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)

    async with async_playwright() as p:
        print("\nSTEP 1: CAPTURING HEX.CO SCREENSHOT")
        print("="*70)

        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(120000)

        # Capture hex.co
        print("\nNavigating to hex.co...")
        await page.goto('https://www.hex.co', wait_until="networkidle")
        await page.wait_for_timeout(3000)

        print("Scrolling to load all content...")
        await scroll_to_bottom(page)

        print("Taking full-page screenshot...")
        await page.screenshot(path=screenshot_name, full_page=True)
        print(f"Screenshot saved: {screenshot_name}")

        # Now go to Miro
        print("\nSTEP 2: ACCESSING MIRO")
        print("="*70)

        print("\nNavigating to Miro login...")
        await page.goto('https://miro.com/login/')
        await page.wait_for_timeout(2000)

        print("\n" + "="*70)
        print("PLEASE LOG IN TO MIRO")
        print("="*70)
        print("\nLog into Miro in the browser window.")
        print("The automation will continue once you reach the dashboard...")
        print("Waiting up to 2 minutes...\n")

        # Wait for login
        try:
            await page.wait_for_url('**/app/dashboard/**', timeout=120000)
            print("- Login successful!")
        except:
            if '/app/' in page.url:
                print("- Miro app detected")
                await page.goto('https://miro.com/app/dashboard/')
                await page.wait_for_timeout(3000)
            else:
                print(f"Current URL: {page.url}")
                return

        print("\nSTEP 3: CREATING BOARD")
        print("="*70)

        await page.wait_for_timeout(2000)

        # Click Create new
        print("\nCreating new board...")
        await page.click('button:has-text("Create new"), button:has-text("Create")')
        await page.wait_for_timeout(3000)

        await page.click('text="Blank board"')
        await page.wait_for_timeout(8000)

        await page.wait_for_url('**/app/board/**', timeout=20000)
        board_url = page.url
        print(f"- Board created: {board_url}")

        # Set board name
        print("\nSTEP 4: NAMING BOARD")
        print("="*70)

        board_name = "test for home screen"
        await page.wait_for_timeout(2000)

        await page.evaluate(f'''
            const titleInputs = document.querySelectorAll('input[placeholder*="Untitled"], input[placeholder*="title"]');
            for (const el of titleInputs) {{
                el.value = "{board_name}";
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        ''')
        print(f"- Board named: {board_name}")

        await page.wait_for_timeout(2000)

        # Upload screenshot
        print("\nSTEP 5: UPLOADING SCREENSHOT")
        print("="*70)

        # Focus and trigger upload
        await page.bring_to_front()
        await page.wait_for_timeout(1000)
        await page.click('body')
        await page.wait_for_timeout(500)

        print("\nOpening file upload dialog...")
        await page.keyboard.press('Control+U')
        await page.wait_for_timeout(2000)

        # Use OS automation to select file
        print("Selecting file with OS automation...")
        time.sleep(2)

        pyautogui.write(screenshot_path, interval=0.05)
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(3)

        print("- Screenshot uploaded!")
        await page.wait_for_timeout(8000)

        print("\n" + "="*70)
        print("- COMPLETE!")
        print("="*70)
        print(f"\nBoard Name: {board_name}")
        print(f"Board URL: {board_url}")
        print(f"Screenshot: hex.co homepage")

        print("\nBrowser staying open for 30 seconds to verify...")
        await page.wait_for_timeout(30000)

        await browser.close()

        # Clean up
        if os.path.exists(screenshot_name):
            os.remove(screenshot_name)
            print(f"\n- Cleaned up: {screenshot_name}")

if __name__ == "__main__":
    asyncio.run(main())
