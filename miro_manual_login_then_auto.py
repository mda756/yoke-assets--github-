import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    print("="*70)
    print("MIRO BOARD - MANUAL LOGIN + AUTO UPLOAD")
    print("="*70)

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

    screenshot_paths = []
    for filename in screenshots:
        if os.path.exists(filename):
            screenshot_paths.append(os.path.abspath(filename))

    print(f"\nFound {len(screenshot_paths)} screenshot files ready")

    async with async_playwright() as p:
        print("\nLaunching browser...")
        browser = await p.chromium.launch(headless=False, slow_mo=800)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(120000)

        # Go to Miro login
        print("\nOpening Miro login page...")
        await page.goto('https://miro.com/login/')
        await page.wait_for_timeout(2000)

        print("\n" + "="*70)
        print("PLEASE LOG IN TO MIRO MANUALLY")
        print("="*70)
        print("\n1. Log into Miro in the browser window that just opened")
        print("2. Wait until you see your dashboard")
        print("3. The automation will continue automatically")
        print("\nWaiting for login... (up to 2 minutes)")

        # Wait for user to login and reach dashboard
        try:
            await page.wait_for_url('**/app/dashboard/**', timeout=120000)
            print("\n  Login successful! Dashboard detected.")
        except:
            # Check if we're on a board or other Miro page
            current_url = page.url
            if '/app/' in current_url:
                print(f"\n  Detected Miro app page: {current_url}")
                # Navigate to dashboard
                print("  Navigating to dashboard...")
                await page.goto('https://miro.com/app/dashboard/')
                await page.wait_for_timeout(3000)
            else:
                print(f"\n  Timeout or not on dashboard. Current URL: {current_url}")
                print("  Trying to continue anyway...")

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
            await page.wait_for_timeout(6000)

            # Wait for board to load
            await page.wait_for_url('**/app/board/**', timeout=20000)
            board_url = page.url
            print(f"3. Board created successfully!")
            print(f"   URL: {board_url}")

            # Set board name
            print("\n4. Setting board name...")
            await page.wait_for_timeout(2000)

            board_name = "Yoke Health Website Screens"

            # Try to find and set title
            try:
                # Look for title element
                title_selectors = [
                    'text="Untitled"',
                    'input[placeholder*="Untitled"]',
                    'input[placeholder*="title"]',
                ]

                renamed = False
                for selector in title_selectors:
                    try:
                        await page.click(selector, timeout=3000)
                        await page.wait_for_timeout(500)
                        # Clear existing text
                        await page.keyboard.press('Control+A')
                        await page.keyboard.type(board_name)
                        await page.keyboard.press('Enter')
                        print(f"   Board renamed to: {board_name}")
                        renamed = True
                        break
                    except:
                        continue

                if not renamed:
                    print("   Could not find title field - you can rename manually")

            except Exception as e:
                print(f"   Title setting: {str(e)[:100]}")

            await page.wait_for_timeout(2000)

            # Upload screenshots
            print(f"\n5. Uploading {len(screenshot_paths)} screenshots...")
            print("   This may take a moment...")

            try:
                # Click on the board canvas to make sure it's focused
                await page.click('body')
                await page.wait_for_timeout(500)

                # Press + to open toolbar
                await page.keyboard.press('+')
                await page.wait_for_timeout(1500)

                # Look for Image or Upload button
                image_button_selectors = [
                    'button:has-text("Image")',
                    'text="Image"',
                    '[aria-label*="Image"]',
                    '[data-testid*="image"]'
                ]

                clicked_image = False
                for selector in image_button_selectors:
                    try:
                        await page.click(selector, timeout=3000)
                        print("   Clicked Image button")
                        clicked_image = True
                        await page.wait_for_timeout(1000)
                        break
                    except:
                        continue

                if not clicked_image:
                    # Try Ctrl+U as fallback
                    print("   Trying Ctrl+U shortcut...")
                    await page.keyboard.press('Control+U')
                    await page.wait_for_timeout(1000)

                # Wait for file input and upload all files
                file_input = await page.wait_for_selector('input[type="file"]', timeout=10000)
                await file_input.set_input_files(screenshot_paths)
                print(f"   All {len(screenshot_paths)} files uploaded!")

                # Wait for uploads to process
                await page.wait_for_timeout(10000)

                print("\n" + "="*70)
                print("SUCCESS!")
                print("="*70)
                print(f"\nBoard: Yoke Health Website Screens")
                print(f"URL: {board_url}")
                print(f"Screenshots: {len(screenshot_paths)} uploaded")
                print("\nThe board is ready in your browser window!")

            except Exception as e:
                print(f"\n   Upload error: {str(e)[:300]}")
                print("\n   MANUAL UPLOAD INSTRUCTIONS:")
                print("   1. Press + on the board")
                print("   2. Click 'Image'")
                print("   3. Select all 7 PNG files from:")
                print(f"      {os.getcwd()}")

        except Exception as e:
            print(f"\nError: {str(e)[:300]}")
            await page.screenshot(path='miro_error.png')

        print("\nBrowser will stay open for 2 minutes for review...")
        await page.wait_for_timeout(120000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
