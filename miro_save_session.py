import asyncio
from playwright.async_api import async_playwright
import pyautogui
import time
import os
import json

async def main():
    print("="*70)
    print("MIRO - ONE-TIME LOGIN + SAVE SESSION FOR FUTURE")
    print("="*70)

    screenshot_name = "hex_co_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)

    if not os.path.exists(screenshot_name):
        print(f"\nERROR: Screenshot not found: {screenshot_path}")
        return

    print(f"\nScreenshot ready: {screenshot_name}")

    # Path to save authentication state
    auth_file = "miro_auth_state.json"

    async with async_playwright() as p:
        print("\nLaunching browser...")
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(120000)

        print("\nNavigating to Miro...")
        await page.goto('https://miro.com/login/')
        await page.wait_for_timeout(3000)

        # Handle cookies
        print("Handling cookies banner...")
        try:
            await page.click('button:has-text("Accept All Cookies"), button:has-text("Accept all"), button:has-text("Accept")', timeout=3000)
            await page.wait_for_timeout(1000)
        except:
            pass

        print("\n" + "="*70)
        print("PLEASE LOG IN TO MIRO NOW")
        print("="*70)
        print("\nYou have 5 MINUTES to complete login.")
        print("After this ONE login, all future operations will be automatic!")
        print("\nWaiting for login...\n")

        # Wait up to 5 minutes for login
        login_successful = False
        try:
            await page.wait_for_url('**/app/dashboard/**', timeout=300000)
            print("Login detected! Dashboard reached.")
            login_successful = True
        except:
            if '/app/' in page.url:
                print(f"Miro app detected: {page.url}")
                await page.goto('https://miro.com/app/dashboard/')
                await page.wait_for_timeout(3000)
                login_successful = True
            else:
                print(f"Login timeout. Current URL: {page.url}")
                await browser.close()
                return

        if not login_successful:
            await browser.close()
            return

        # SAVE THE AUTHENTICATION STATE
        print("\nSaving authentication state for future use...")
        storage_state = await context.storage_state()
        with open(auth_file, 'w') as f:
            json.dump(storage_state, f)
        print(f"Authentication saved to: {auth_file}")
        print("Future runs will use this automatically!")

        await page.wait_for_timeout(2000)

        # Now proceed with creating board
        print("\n" + "="*70)
        print("CREATING BOARD AUTOMATICALLY")
        print("="*70)

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
        print(f"Board named: {board_name}")
        await page.wait_for_timeout(2000)

        # Upload screenshot
        print("\nUploading screenshot...")
        await page.bring_to_front()
        await page.wait_for_timeout(1000)
        await page.click('body')
        await page.wait_for_timeout(500)

        await page.keyboard.press('Control+U')
        await page.wait_for_timeout(2000)

        print("  Using OS automation...")
        time.sleep(2)
        pyautogui.write(screenshot_path, interval=0.05)
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(3)

        print("  Upload complete!")
        await page.wait_for_timeout(8000)

        print("\n" + "="*70)
        print("SUCCESS!")
        print("="*70)
        print(f"\nBoard: {board_name}")
        print(f"URL: {board_url}")
        print("Screenshot: hex.co homepage")
        print(f"\nAuthentication saved! Future Miro operations will be fully automatic.")

        print("\nBrowser staying open for 30 seconds...")
        await page.wait_for_timeout(30000)
        await browser.close()

        # Clean up
        if os.path.exists(screenshot_name):
            os.remove(screenshot_name)
            print(f"\nCleaned up: {screenshot_name}")

if __name__ == "__main__":
    asyncio.run(main())
