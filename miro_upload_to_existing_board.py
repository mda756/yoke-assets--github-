import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    print("="*70)
    print("UPLOAD TO EXISTING MIRO BOARD")
    print("="*70)

    # Existing board URL from previous successful creation
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

    screenshot_paths = [os.path.abspath(f) for f in screenshots if os.path.exists(f)]
    print(f"\nFound {len(screenshot_paths)} screenshots ready to upload")
    print(f"Target board: {board_url}")

    async with async_playwright() as p:
        print("\nLaunching browser...")
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(120000)

        # Navigate to the board
        print("\nOpening Miro board...")
        await page.goto(board_url)
        await page.wait_for_timeout(5000)

        # Check if we need to login
        current_url = page.url
        if 'login' in current_url or 'signup' in current_url:
            print("\n" + "="*70)
            print("LOGIN REQUIRED")
            print("="*70)
            print("\nPlease log into Miro in the browser window.")
            print("The automation will continue once you're logged in...")
            print("Waiting up to 2 minutes...\n")

            # Wait for login
            try:
                await page.wait_for_url(f'**{board_url}**', timeout=120000)
                print("Login successful!")
            except:
                print("Still waiting... checking current state...")
                if '/app/board/' in page.url:
                    print("Detected board page, continuing...")
                else:
                    print(f"Current URL: {page.url}")
                    print("Attempting to navigate to board...")
                    await page.goto(board_url)
                    await page.wait_for_timeout(5000)

        print("\n" + "="*70)
        print("RENAMING BOARD")
        print("="*70)

        board_name = "Yoke Health Website Screens"

        # Rename board using multiple methods
        try:
            # Method 1: Click on title
            print("\nAttempting to rename board...")
            await page.wait_for_timeout(2000)

            # Try clicking on Untitled text
            try:
                await page.click('text="Untitled"', timeout=5000)
                await page.wait_for_timeout(500)
                await page.keyboard.press('Control+A')
                await page.keyboard.type(board_name)
                await page.keyboard.press('Enter')
                print(f"Board renamed to: {board_name}")
            except:
                # Try JavaScript method
                await page.evaluate(f'''
                    const titleElements = document.querySelectorAll('input[placeholder*="Untitled"], input[placeholder*="title"]');
                    for (const el of titleElements) {{
                        el.value = "{board_name}";
                        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                ''')
                print(f"Board name set via JavaScript: {board_name}")

            await page.wait_for_timeout(1000)

        except Exception as e:
            print(f"Rename attempt: {str(e)[:100]}")

        print("\n" + "="*70)
        print("UPLOADING SCREENSHOTS")
        print("="*70)

        print(f"\nUploading {len(screenshot_paths)} files...")

        # Upload method: Try to use native Miro upload
        try:
            # Click on board to focus
            await page.click('body')
            await page.wait_for_timeout(500)

            # Open upload dialog - try keyboard shortcut
            print("\n1. Opening upload dialog...")
            await page.keyboard.press('Control+U')
            await page.wait_for_timeout(2000)

            # Look for file input
            file_inputs = await page.query_selector_all('input[type="file"]')

            if not file_inputs:
                # Try pressing + and clicking Image
                print("2. Trying + menu...")
                await page.keyboard.press('+')
                await page.wait_for_timeout(1500)

                # Click Image
                try:
                    await page.click('button:has-text("Image"), text="Image"', timeout=5000)
                    await page.wait_for_timeout(1000)
                except:
                    print("   Could not find Image button")

                file_inputs = await page.query_selector_all('input[type="file"]')

            if file_inputs:
                print(f"3. File input found, uploading all {len(screenshot_paths)} files...")
                await file_inputs[0].set_input_files(screenshot_paths)
                print("   Files uploaded!")
                await page.wait_for_timeout(10000)  # Wait for upload to complete

                print("\n" + "="*70)
                print("SUCCESS!")
                print("="*70)
                print(f"\nBoard: {board_name}")
                print(f"URL: {board_url}")
                print(f"Screenshots uploaded: {len(screenshot_paths)}")

            else:
                print("\nCould not find file input.")
                print("\nMANUAL UPLOAD STEPS:")
                print("1. In the Miro board, press Ctrl+U or press +")
                print("2. Click 'Image'")
                print("3. Select all files from:")
                print(f"   {os.getcwd()}")
                print("\nFiles to upload:")
                for path in screenshot_paths:
                    print(f"   - {os.path.basename(path)}")

        except Exception as e:
            print(f"\nUpload error: {str(e)[:300]}")
            print("\nThe board is open - please upload manually using the steps above.")

        print("\nBrowser staying open for 2 minutes for review...")
        await page.wait_for_timeout(120000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
