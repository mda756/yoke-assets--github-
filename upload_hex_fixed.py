import asyncio
from playwright.async_api import async_playwright
import pyautogui
import time
import os

async def main():
    print("="*70)
    print("UPLOAD HEX.CO TO MIRO - FIXED WITH COOKIE HANDLING")
    print("="*70)

    screenshot_name = "hex_co_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)

    if not os.path.exists(screenshot_name):
        print(f"\nERROR: Screenshot not found: {screenshot_path}")
        return

    print(f"\nScreenshot ready: {screenshot_name}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(120000)

        print("\nOpening Miro login...")
        await page.goto('https://miro.com/login/')
        await page.wait_for_timeout(3000)

        # Handle cookies banner - try multiple selectors
        print("Handling cookies banner...")
        cookie_selectors = [
            'button:has-text("Accept All Cookies")',
            'button:has-text("Accept all")',
            'button:has-text("Accept")',
            '[data-testid="cookieBanner.button.acceptAll"]',
            'button[id*="accept"]',
            'button[class*="accept"]'
        ]

        for selector in cookie_selectors:
            try:
                await page.click(selector, timeout=3000)
                print(f"  Clicked cookies button: {selector}")
                await page.wait_for_timeout(1000)
                break
            except:
                continue

        # Check for other blocking overlays/modals
        print("Checking for other overlays...")
        await page.wait_for_timeout(2000)

        # Try to close any modals/popups
        close_selectors = [
            'button[aria-label="Close"]',
            'button:has-text("Close")',
            '[data-testid="modal-close"]',
            '.close-button'
        ]

        for selector in close_selectors:
            try:
                await page.click(selector, timeout=2000)
                print(f"  Closed overlay: {selector}")
                await page.wait_for_timeout(500)
            except:
                continue

        # Now proceed with login
        print("\n" + "="*70)
        print("READY FOR LOGIN")
        print("="*70)
        print("\nPlease log in to Miro now.")
        print("All blocking screens should be cleared.")
        print("Waiting up to 3 minutes...\n")

        # Wait for login with longer timeout
        login_successful = False
        try:
            await page.wait_for_url('**/app/dashboard/**', timeout=180000)
            print("Login successful! Dashboard reached.")
            login_successful = True
        except:
            current_url = page.url
            print(f"Login timeout. Current URL: {current_url}")

            # Check if we're on any Miro app page
            if '/app/' in current_url:
                print("Detected Miro app page - navigating to dashboard...")
                await page.goto('https://miro.com/app/dashboard/')
                await page.wait_for_timeout(4000)
                login_successful = True
            else:
                print("\nCould not detect successful login.")
                print("Browser staying open - please complete login manually.")
                print("Then close browser and run script again.")
                await page.wait_for_timeout(60000)
                await browser.close()
                return

        if not login_successful:
            return

        await page.wait_for_timeout(2000)

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
        print("\nSetting board name...")
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
        print("\nUploading hex.co screenshot...")
        await page.bring_to_front()
        await page.wait_for_timeout(1000)
        await page.click('body')
        await page.wait_for_timeout(500)

        print("  Opening file dialog (Ctrl+U)...")
        await page.keyboard.press('Control+U')
        await page.wait_for_timeout(2000)

        print("  Selecting file with OS automation...")
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
        print(f"\nBoard Name: {board_name}")
        print(f"Board URL: {board_url}")
        print("Screenshot: hex.co homepage uploaded")

        print("\nBrowser staying open for 30 seconds to verify...")
        await page.wait_for_timeout(30000)
        await browser.close()

        # Clean up
        if os.path.exists(screenshot_name):
            os.remove(screenshot_name)
            print(f"\nCleaned up temp file: {screenshot_name}")

if __name__ == "__main__":
    asyncio.run(main())
