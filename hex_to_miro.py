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
    print("HEX.CO TO MIRO - FULL AUTOMATION")
    print("="*70)

    screenshot_name = "hex_co_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)

    async with async_playwright() as p:
        print("\n1. CAPTURING HEX.CO SCREENSHOT")
        print("="*70)

        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(90000)

        # Capture hex.co screenshot
        print("\nNavigating to hex.co...")
        await page.goto('https://www.hex.co', wait_until="networkidle")
        await page.wait_for_timeout(3000)

        print("Scrolling to load all content...")
        await scroll_to_bottom(page)

        print("Taking full-page screenshot...")
        await page.screenshot(path=screenshot_name, full_page=True)
        print(f"Screenshot saved: {screenshot_name}")

        # Now create Miro board
        print("\n2. CREATING MIRO BOARD")
        print("="*70)

        # Try direct link first
        miro_link = "https://click.miro.com/f/a/yozjFXntXQNNQuQ6FMeuYg~~/AAAHahA~/odFBR-uKawzwUVbZGS7JDaH7B6Ll_D2x3BQT0nkLCZrnzLGZq8LiR4uOEAigb9J5KTD3YAEXk96jvZmQiamqXD5qG908lSJ_-wjclGfIZkJT8SUdttn_-eDBBUXDVcCx665RWbMTZDkGgHk_me8v6sp96Zkrm0XH9h0x1NLROYsuadhEBABUfcgnLC3xvT5yiD9Wolx6pF5LCQDPjZ4rAU2qjlNRQqXe6SvEa0MGhw2KWmKhZO9UCCGZuj29xJokAxUjUHu_wGusGPV9_vx2oBG_AFx5ryqnKkej8UvCOvA~"

        print("\nAccessing Miro...")
        await page.goto(miro_link)
        await page.wait_for_timeout(5000)

        # Check if we need login
        if 'dashboard' not in page.url and 'board' not in page.url:
            print("Login required - please log in...")
            print("Waiting up to 2 minutes...")
            try:
                await page.wait_for_url('**/app/dashboard/**', timeout=120000)
                print("Login successful!")
            except:
                if '/app/' in page.url:
                    print("Miro app detected, continuing...")
                else:
                    print(f"Current URL: {page.url}")
                    await page.goto('https://miro.com/app/dashboard/')
                    await page.wait_for_timeout(3000)

        # Make sure we're on dashboard
        if 'dashboard' not in page.url:
            print("Navigating to dashboard...")
            await page.goto('https://miro.com/app/dashboard/')
            await page.wait_for_timeout(4000)

        # Create new board
        print("\nCreating new board...")
        await page.click('button:has-text("Create new"), button:has-text("Create")')
        await page.wait_for_timeout(3000)

        await page.click('text="Blank board"')
        await page.wait_for_timeout(8000)

        # Wait for board to load
        await page.wait_for_url('**/app/board/**', timeout=20000)
        board_url = page.url
        print(f"Board created: {board_url}")

        # Set board name
        print("\n3. NAMING BOARD")
        print("="*70)

        board_name = "test for home screen"
        await page.wait_for_timeout(2000)

        try:
            await page.evaluate(f'''
                const titleInputs = document.querySelectorAll('input[placeholder*="Untitled"], input[placeholder*="title"]');
                for (const el of titleInputs) {{
                    el.value = "{board_name}";
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            ''')
            print(f"Board named: {board_name}")
        except Exception as e:
            print(f"Naming: {str(e)[:100]}")

        await page.wait_for_timeout(2000)

        # Upload screenshot
        print("\n4. UPLOADING SCREENSHOT")
        print("="*70)

        # Focus browser
        await page.bring_to_front()
        await page.wait_for_timeout(1000)
        await page.click('body')
        await page.wait_for_timeout(500)

        # Trigger upload dialog
        print("\nOpening file upload dialog (Ctrl+U)...")
        await page.keyboard.press('Control+U')
        await page.wait_for_timeout(2000)

        # Use OS automation to select file
        print("Using OS automation to select file...")
        time.sleep(2)

        try:
            # Type the full file path
            print(f"   Typing file path...")
            pyautogui.write(screenshot_path, interval=0.05)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(3)

            print("   Screenshot uploaded!")

            # Wait for upload to process
            await page.wait_for_timeout(8000)

            print("\n" + "="*70)
            print("COMPLETE!")
            print("="*70)
            print(f"\nBoard: {board_name}")
            print(f"URL: {board_url}")
            print(f"Screenshot: hex.co homepage uploaded")

        except Exception as e:
            print(f"\nOS automation: {str(e)}")

        print("\nBrowser staying open for 30 seconds to verify...")
        await page.wait_for_timeout(30000)

        await browser.close()

        # Clean up screenshot file
        if os.path.exists(screenshot_name):
            os.remove(screenshot_name)
            print(f"\nCleaned up temporary file: {screenshot_name}")

if __name__ == "__main__":
    asyncio.run(main())
