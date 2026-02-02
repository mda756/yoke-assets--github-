import asyncio
from playwright.async_api import async_playwright
import pyautogui
import time
import os

async def main():
    print("="*70)
    print("UPLOAD HEX.CO TO MIRO - USING YOUR CHROME PROFILE")
    print("="*70)

    screenshot_name = "hex_co_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)

    if not os.path.exists(screenshot_name):
        print(f"\nERROR: Screenshot not found: {screenshot_path}")
        return

    print(f"\nScreenshot ready: {screenshot_name}")

    # Use user's Chrome profile to access saved passwords
    user_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")
    print(f"\nUsing Chrome profile: {user_data_dir}")

    async with async_playwright() as p:
        print("\nLaunching Chrome with your profile...")

        # Launch with user's Chrome profile
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            slow_mo=500,
            channel="chrome",
            args=['--no-first-run', '--no-default-browser-check']
        )

        page = context.pages[0] if context.pages else await context.new_page()
        page.set_default_timeout(120000)

        print("\nNavigating to Miro...")
        await page.goto('https://miro.com/login/')
        await page.wait_for_timeout(3000)

        # Handle cookies
        print("Handling cookies...")
        try:
            await page.click('button:has-text("Accept All Cookies"), button:has-text("Accept all"), button:has-text("Accept")', timeout=3000)
            print("  Cookies accepted")
            await page.wait_for_timeout(1000)
        except:
            print("  No cookies banner found")

        # Check if already logged in
        await page.wait_for_timeout(2000)
        current_url = page.url

        if '/app/dashboard' in current_url or '/app/board' in current_url:
            print("\nAlready logged in! Proceeding to dashboard...")
            if '/app/dashboard' not in current_url:
                await page.goto('https://miro.com/app/dashboard/')
                await page.wait_for_timeout(3000)
        else:
            print("\nAttempting Google login...")

            # Look for and click Google sign-in button
            try:
                # Try to find Google sign-in button
                google_button = await page.wait_for_selector('button:has-text("Google"), [aria-label*="Google"]', timeout=5000)
                await google_button.click()
                print("  Clicked Google sign-in")
                await page.wait_for_timeout(3000)

                # Google should auto-login with saved credentials
                print("  Waiting for Google authentication...")
                await page.wait_for_timeout(5000)

            except:
                print("  Could not find Google button, checking login state...")

            # Wait for dashboard
            print("\nWaiting for dashboard...")
            try:
                await page.wait_for_url('**/app/dashboard/**', timeout=60000)
                print("Dashboard reached!")
            except:
                if '/app/' in page.url:
                    print(f"On Miro app page: {page.url}")
                    await page.goto('https://miro.com/app/dashboard/')
                    await page.wait_for_timeout(3000)
                else:
                    print(f"Not logged in. Current URL: {page.url}")
                    print("Please complete login manually in the browser.")
                    print("Waiting 2 minutes...")
                    await page.wait_for_timeout(120000)

                    if '/app/dashboard' not in page.url:
                        await context.close()
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

        print("\nBrowser staying open for 30 seconds...")
        await page.wait_for_timeout(30000)
        await context.close()

        # Clean up
        if os.path.exists(screenshot_name):
            os.remove(screenshot_name)
            print(f"\nCleaned up: {screenshot_name}")

if __name__ == "__main__":
    asyncio.run(main())
