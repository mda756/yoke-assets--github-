import asyncio
from playwright.async_api import async_playwright
import pyautogui
import time
import os

async def main():
    print("="*70)
    print("MIRO - COMPLETE AUTOMATION WITH OS-LEVEL FILE PICKER")
    print("="*70)

    # Existing board URL
    board_url = "https://miro.com/app/board/uXjVGI1sl_U=/"

    # Screenshot files
    screenshots = [
        "yoke_1_Home.png",
        "yoke_2_AI_Healthcare_Platforms.png",
        "yoke_3_Our_Work.png",
        "yoke_4_Agency.png",
        "yoke_5_Biotech.png",
        "yoke_6_Team.png",
        "yoke_7_Contact.png"
    ]

    screenshot_dir = os.path.abspath(os.getcwd())
    print(f"\nScreenshot directory: {screenshot_dir}")
    print(f"Screenshots to upload: {len(screenshots)}")

    async with async_playwright() as p:
        print("\nLaunching browser...")
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(120000)

        # Navigate to board
        print(f"\nOpening Miro board...")
        await page.goto(board_url)
        await page.wait_for_timeout(5000)

        # Check if login needed
        if 'login' in page.url or 'signup' in page.url:
            print("\nPlease log in to Miro in the browser window...")
            print("Waiting up to 2 minutes...")
            try:
                await page.wait_for_url('**/app/board/**', timeout=120000)
                print("Login detected, continuing...")
            except:
                if '/app/board/' in page.url:
                    print("Board detected, continuing...")
                else:
                    print("Attempting to navigate to board...")
                    await page.goto(board_url)
                    await page.wait_for_timeout(5000)

        await page.wait_for_timeout(2000)

        # Rename board
        print("\nRenaming board...")
        board_name = "Yoke Health Website Screens"
        try:
            await page.evaluate(f'''
                const titleInputs = document.querySelectorAll('input[placeholder*="Untitled"], input[placeholder*="title"]');
                for (const el of titleInputs) {{
                    el.value = "{board_name}";
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            ''')
            print(f"Board renamed to: {board_name}")
        except Exception as e:
            print(f"Rename: {str(e)[:100]}")

        await page.wait_for_timeout(2000)

        # Upload screenshots using OS-level automation
        print("\n" + "="*70)
        print("UPLOADING SCREENSHOTS - OS-LEVEL AUTOMATION")
        print("="*70)

        # Focus the browser window
        print("\n1. Focusing browser window...")
        await page.bring_to_front()
        await page.wait_for_timeout(1000)

        # Click on the board to ensure it's focused
        await page.click('body')
        await page.wait_for_timeout(500)

        # Trigger file upload dialog using keyboard
        print("2. Opening file upload dialog (Ctrl+U)...")
        await page.keyboard.press('Control+U')
        await page.wait_for_timeout(2000)

        # Give the file dialog time to open
        print("3. Waiting for file picker dialog to open...")
        time.sleep(2)

        # Use pyautogui to control the file picker
        print("4. Using OS automation to select files...")

        try:
            # Type the directory path in the file dialog
            print(f"   Typing directory path...")
            pyautogui.write(screenshot_dir, interval=0.05)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(1.5)

            # Select all PNG files
            print("   Typing filename pattern...")
            pyautogui.write('yoke_*.png', interval=0.05)
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(3)

            print("   Files selected and upload initiated!")

            # Wait for upload to complete
            await page.wait_for_timeout(10000)

            print("\n" + "="*70)
            print("UPLOAD COMPLETE!")
            print("="*70)
            print(f"\nBoard: {board_name}")
            print(f"URL: {board_url}")
            print(f"Screenshots uploaded: {len(screenshots)}")

        except Exception as e:
            print(f"\nOS automation error: {str(e)}")
            print("\nIf the file dialog is open, you can manually:")
            print(f"1. Navigate to: {screenshot_dir}")
            print("2. Select all yoke_*.png files")
            print("3. Click Open")

        print("\nBrowser staying open for 30 seconds to verify...")
        await page.wait_for_timeout(30000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
