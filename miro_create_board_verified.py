import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    print("="*70)
    print("MIRO BOARD CREATION - VERIFIED APPROACH")
    print("="*70)

    # Direct Miro link
    miro_link = "https://click.miro.com/f/a/yozjFXntXQNNQuQ6FMeuYg~~/AAAHahA~/odFBR-uKawzwUVbZGS7JDaH7B6Ll_D2x3BQT0nkLCZrnzLGZq8LiR4uOEAigb9J5KTD3YAEXk96jvZmQiamqXD5qG908lSJ_-wjclGfIZkJT8SUdttn_-eDBBUXDVcCx665RWbMTZDkGgHk_me8v6sp96Zkrm0XH9h0x1NLROYsuadhEBABUfcgnLC3xvT5yiD9Wolx6pF5LCQDPjZ4rAU2qjlNRQqXe6SvEa0MGhw2KWmKhZO9UCCGZuj29xJokAxUjUHu_wGusGPV9_vx2oBG_AFx5ryqnKkej8UvCOvA~"

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
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(90000)

        # Navigate to Miro
        print("\nAccessing Miro...")
        await page.goto(miro_link)
        await page.wait_for_timeout(5000)

        current_url = page.url
        print(f"Current URL: {current_url}")

        # Make sure we're on dashboard
        if 'dashboard' not in current_url:
            print("Navigating to dashboard...")
            await page.goto('https://miro.com/app/dashboard/')
            await page.wait_for_timeout(3000)

        # Take screenshot of dashboard
        await page.screenshot(path='miro_before_create.png')
        print("Dashboard screenshot saved")

        # Create new board - more careful approach
        print("\nCreating new board...")
        try:
            # Look for the Create new button
            create_button = await page.wait_for_selector('button:has-text("Create new"), button:has-text("Create")', timeout=10000)
            await create_button.click()
            print("  Clicked 'Create new' button")
            await page.wait_for_timeout(3000)

            # Look for Blank board option
            blank_board = await page.wait_for_selector('text="Blank board"', timeout=10000)
            await blank_board.click()
            print("  Clicked 'Blank board'")
            await page.wait_for_timeout(5000)

            # Wait for board to load - look for board URL
            await page.wait_for_url('**/app/board/**', timeout=20000)
            board_url = page.url
            print(f"  Board created! URL: {board_url}")

            # Wait for board to fully load
            await page.wait_for_timeout(3000)

            # Set board title - try multiple methods
            print("\nSetting board title...")
            board_name = "Yoke Health Website Screens"

            # Method 1: Look for title input at top
            try:
                # Click on the board title area (usually says "Untitled")
                title_element = await page.query_selector('input[placeholder*="Untitled"], input[placeholder*="title"], [data-testid*="board-title"]')
                if title_element:
                    await title_element.click()
                    await page.wait_for_timeout(500)
                    await title_element.fill(board_name)
                    await page.keyboard.press('Enter')
                    print(f"  Title set to: {board_name}")
                else:
                    # Try clicking near top left where title usually is
                    await page.click('text="Untitled"', timeout=5000)
                    await page.wait_for_timeout(500)
                    await page.keyboard.type(board_name)
                    await page.keyboard.press('Enter')
                    print(f"  Title set to: {board_name}")
            except Exception as e:
                print(f"  Could not set title: {str(e)[:100]}")
                print("  You can rename manually")

            await page.wait_for_timeout(2000)

            # Take screenshot of empty board
            await page.screenshot(path='miro_board_created.png')
            print("  Board screenshot saved")

            # Now upload screenshots
            print(f"\nUploading {len(screenshot_paths)} screenshots...")

            # Upload all files at once (more reliable)
            try:
                # Try to find or trigger file upload
                print("  Looking for upload mechanism...")

                # Try pressing + key or click on toolbar
                await page.keyboard.press('+')
                await page.wait_for_timeout(1000)

                # Look for upload/image option
                upload_selectors = [
                    'button:has-text("Image")',
                    'button:has-text("Upload")',
                    '[data-testid*="upload"]',
                    '[aria-label*="Image"]',
                    '[aria-label*="Upload"]'
                ]

                clicked_upload = False
                for selector in upload_selectors:
                    try:
                        await page.click(selector, timeout=2000)
                        print(f"  Clicked upload button: {selector}")
                        clicked_upload = True
                        await page.wait_for_timeout(1000)
                        break
                    except:
                        continue

                if not clicked_upload:
                    # Try keyboard shortcut
                    print("  Trying Ctrl+U shortcut...")
                    await page.keyboard.press('Control+U')
                    await page.wait_for_timeout(1000)

                # Look for file input
                file_input = await page.wait_for_selector('input[type="file"]', timeout=5000)
                if file_input:
                    # Upload all screenshots at once
                    await file_input.set_input_files(screenshot_paths)
                    print(f"  Uploaded all {len(screenshot_paths)} files!")
                    await page.wait_for_timeout(5000)

                    # Take screenshot after upload
                    await page.screenshot(path='miro_after_upload.png')
                    print("  Post-upload screenshot saved")
                else:
                    print("  Could not find file input")

            except Exception as e:
                print(f"  Upload error: {str(e)[:200]}")

            print("\n" + "="*70)
            print("BOARD CREATION COMPLETE")
            print("="*70)
            print(f"\nBoard URL: {board_url}")
            print(f"Board name: {board_name}")
            print(f"Screenshots uploaded: {len(screenshot_paths)}")
            print("\nCheck the browser window to verify everything looks good.")
            print("\nIf screenshots didn't upload automatically, you can:")
            print("1. Press + on the board")
            print("2. Select 'Image' or 'Upload'")
            print("3. Select all PNG files from:")
            print(f"   {os.getcwd()}")

        except Exception as e:
            print(f"\nError during board creation: {str(e)[:300]}")
            print("\nCurrent page screenshot saved for debugging")
            await page.screenshot(path='miro_error_state.png')

        print("\nBrowser staying open for 2 minutes for manual review...")
        await page.wait_for_timeout(120000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
