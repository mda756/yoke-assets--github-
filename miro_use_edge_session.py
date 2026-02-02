import asyncio
from playwright.async_api import async_playwright
import pyautogui
import time
import os

async def main():
    print("="*70)
    print("MIRO - USING YOUR EDGE SESSION")
    print("="*70)

    screenshot_name = "hex_co_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)

    if not os.path.exists(screenshot_name):
        print(f"\nERROR: Screenshot not found: {screenshot_path}")
        return

    print(f"\nScreenshot ready: {screenshot_name}")
    print("\nIMPORTANT: Close Microsoft Edge before running this script!")
    print("Proceeding in 5 seconds...")
    import time
    time.sleep(5)

    # Use Edge profile
    edge_profile = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data")
    print(f"\nUsing Edge profile: {edge_profile}")

    async with async_playwright() as p:
        print("\nLaunching Edge with your profile...")

        try:
            context = await p.chromium.launch_persistent_context(
                edge_profile,
                headless=False,
                slow_mo=500,
                channel="msedge",
                args=['--no-first-run']
            )

            page = context.pages[0] if context.pages else await context.new_page()
            page.set_default_timeout(120000)

            print("\nNavigating to Miro dashboard...")
            await page.goto('https://miro.com/app/dashboard/')
            await page.wait_for_timeout(4000)

            # Check if we're logged in
            current_url = page.url
            print(f"Current URL: {current_url}")

            if 'login' in current_url or 'signup' in current_url:
                print("\nNot logged in. Please log in now...")
                print("Waiting 2 minutes...")
                await page.wait_for_timeout(120000)

                if 'dashboard' not in page.url and 'board' not in page.url:
                    print("Login not completed. Exiting...")
                    await context.close()
                    return
            else:
                print("Already logged in!")

            # Make sure we're on dashboard
            if 'dashboard' not in page.url:
                await page.goto('https://miro.com/app/dashboard/')
                await page.wait_for_timeout(3000)

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

        except Exception as e:
            print(f"\nError: {str(e)}")
            print("\nIf Edge is still running, please close it and run this script again.")

if __name__ == "__main__":
    asyncio.run(main())
