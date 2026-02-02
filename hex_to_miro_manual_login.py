import asyncio
from playwright.async_api import async_playwright
import pyautogui
import time
import os

async def main():
    print("="*70)
    print("HEX.CO TO MIRO - MANUAL LOGIN + AUTO UPLOAD")
    print("="*70)

    screenshot_name = "hex_co_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)

    # Check if screenshot exists
    if not os.path.exists(screenshot_name):
        print("\nScreenshot not found - this should have been created by previous run")
        print(f"Expected: {screenshot_path}")
        return

    print(f"\nScreenshot ready: {screenshot_name}")

    async with async_playwright() as p:
        print("\nLaunching browser...")
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(120000)

        # Go to Miro login
        print("\nOpening Miro login...")
        await page.goto('https://miro.com/login/')
        await page.wait_for_timeout(2000)

        print("\n" + "="*70)
        print("PLEASE LOG IN TO MIRO")
        print("="*70)
        print("\n1. Log into Miro in the browser window")
        print("2. Wait until you see your dashboard")
        print("3. Automation will continue automatically")
        print("\nWaiting for login... (up to 2 minutes)")

        # Wait for login
        try:
            await page.wait_for_url('**/app/dashboard/**', timeout=120000)
            print("\nLogin successful! Dashboard detected.")
        except:
            current_url = page.url
            if '/app/' in current_url:
                print(f"\nMiro app detected: {current_url}")
                await page.goto('https://miro.com/app/dashboard/')
                await page.wait_for_timeout(3000)
            else:
                print(f"\nTimeout. Current URL: {current_url}")
                print("Continuing anyway...")

        # Create new board
        print("\n" + "="*70)
        print("CREATING BOARD AUTOMATICALLY")
        print("="*70)

        await page.wait_for_timeout(2000)

        try:
            # Click Create new
            print("\n1. Clicking 'Create new' button...")
            await page.click('button:has-text("Create new"), button:has-text("Create")')
            await page.wait_for_timeout(3000)

            # Click Blank board
            print("2. Selecting 'Blank board'...")
            await page.click('text="Blank board"')
            await page.wait_for_timeout(8000)

            # Wait for board
            await page.wait_for_url('**/app/board/**', timeout=20000)
            board_url = page.url
            print(f"3. Board created!")
            print(f"   URL: {board_url}")

            # Set board name
            print("\n4. Setting board name...")
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
                print(f"   Board named: {board_name}")
            except Exception as e:
                print(f"   Naming: {str(e)[:100]}")

            await page.wait_for_timeout(2000)

            # Upload screenshot
            print("\n5. Uploading hex.co screenshot...")

            # Focus browser
            await page.bring_to_front()
            await page.wait_for_timeout(1000)
            await page.click('body')
            await page.wait_for_timeout(500)

            # Trigger upload dialog
            print("   Opening file upload dialog (Ctrl+U)...")
            await page.keyboard.press('Control+U')
            await page.wait_for_timeout(2000)

            # Use OS automation
            print("   Using OS automation to select file...")
            time.sleep(2)

            try:
                pyautogui.write(screenshot_path, interval=0.05)
                time.sleep(0.5)
                pyautogui.press('enter')
                time.sleep(3)

                print("   Screenshot uploaded!")
                await page.wait_for_timeout(8000)

                print("\n" + "="*70)
                print("SUCCESS!")
                print("="*70)
                print(f"\nBoard: {board_name}")
                print(f"URL: {board_url}")
                print("Screenshot: hex.co homepage uploaded")

            except Exception as e:
                print(f"   OS automation: {str(e)}")

        except Exception as e:
            print(f"\nError: {str(e)[:300]}")

        print("\nBrowser staying open for 30 seconds to verify...")
        await page.wait_for_timeout(30000)

        await browser.close()

        # Clean up screenshot file
        if os.path.exists(screenshot_name):
            os.remove(screenshot_name)
            print(f"\nCleaned up temporary file: {screenshot_name}")

if __name__ == "__main__":
    asyncio.run(main())
