import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    print("="*70)
    print("MIRO DIRECT ACCESS")
    print("="*70)

    # Direct Miro link
    miro_link = "https://click.miro.com/f/a/yozjFXntXQNNQuQ6FMeuYg~~/AAAHahA~/odFBR-uKawzwUVbZGS7JDaH7B6Ll_D2x3BQT0nkLCZrnzLGZq8LiR4uOEAigb9J5KTD3YAEXk96jvZmQiamqXD5qG908lSJ_-wjclGfIZkJT8SUdttn_-eDBBUXDVcCx665RWbMTZDkGgHk_me8v6sp96Zkrm0XH9h0x1NLROYsuadhEBABUfcgnLC3xvT5yiD9Wolx6pF5LCQDPjZ4rAU2qjlNRQqXe6SvEa0MGhw2KWmKhZO9UCCGZuj29xJokAxUjUHu_wGusGPV9_vx2oBG_AFx5ryqnKkej8UvCOvA~"

    # Screenshot files
    screenshots = []
    for i in range(1, 8):
        files = [
            ("yoke_1_Home.png", "Home"),
            ("yoke_2_AI_Healthcare_Platforms.png", "AI Healthcare Platforms"),
            ("yoke_3_Our_Work.png", "Our Work"),
            ("yoke_4_Agency.png", "Agency"),
            ("yoke_5_Biotech.png", "Biotech"),
            ("yoke_6_Team.png", "Team"),
            ("yoke_7_Contact.png", "Contact")
        ]
        if i <= len(files):
            filename = files[i-1][0]
            name = files[i-1][1]
            if os.path.exists(filename):
                screenshots.append({
                    'path': os.path.abspath(filename),
                    'filename': filename,
                    'name': name
                })

    print(f"\nFound {len(screenshots)} screenshot files ready to upload")

    async with async_playwright() as p:
        print("\nLaunching browser...")
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(90000)

        # Navigate to Miro link
        print(f"\nAccessing Miro link...")
        await page.goto(miro_link)
        await page.wait_for_timeout(5000)

        # Check where we landed
        current_url = page.url
        print(f"Current URL: {current_url}")

        # Take screenshot of current page
        await page.screenshot(path='miro_access_result.png', full_page=True)
        print("Saved screenshot: miro_access_result.png")

        # Check if we're on a board or dashboard
        if '/app/board/' in current_url:
            print("\nWe're on a board! Attempting to upload screenshots...")

            # Try to upload files
            for i, screenshot in enumerate(screenshots, 1):
                try:
                    print(f"\nUploading {i}/{len(screenshots)}: {screenshot['filename']}")

                    # Look for file input or try to trigger upload
                    file_inputs = await page.query_selector_all('input[type="file"]')

                    if not file_inputs:
                        # Try keyboard shortcuts
                        print("   Trying Ctrl+U...")
                        await page.keyboard.press('Control+U')
                        await page.wait_for_timeout(1000)
                        file_inputs = await page.query_selector_all('input[type="file"]')

                    if file_inputs:
                        await file_inputs[0].set_input_files(screenshot['path'])
                        print(f"   Uploaded: {screenshot['filename']}")
                        await page.wait_for_timeout(3000)
                    else:
                        print(f"   No file input found, trying drag-drop simulation...")
                        # The file input might be hidden, try to locate it differently
                        await page.evaluate(f'''
                            const input = document.querySelector('input[type="file"]') ||
                                         document.createElement('input');
                            input.type = 'file';
                            input.style.display = 'none';
                            document.body.appendChild(input);
                        ''')
                        await page.wait_for_timeout(500)
                        file_inputs = await page.query_selector_all('input[type="file"]')
                        if file_inputs:
                            await file_inputs[-1].set_input_files(screenshot['path'])
                            print(f"   Uploaded: {screenshot['filename']}")
                            await page.wait_for_timeout(3000)

                except Exception as e:
                    print(f"   Error: {str(e)[:150]}")

            print("\n" + "="*70)
            print("UPLOAD COMPLETE")
            print("="*70)

        elif '/app/dashboard/' in current_url:
            print("\nWe're on the dashboard. Creating new board...")

            # Click create new board
            try:
                await page.click('button:has-text("Create new")', timeout=5000)
                await page.wait_for_timeout(2000)
                await page.click('text="Blank board"', timeout=5000)
                await page.wait_for_timeout(5000)

                # Wait for board
                await page.wait_for_url('**/app/board/**', timeout=15000)
                print("Board created!")

                # Set name
                try:
                    await page.keyboard.type("Yoke Health Website Screens")
                    await page.keyboard.press('Enter')
                except:
                    pass

                # Upload screenshots
                print("\nUploading screenshots...")
                for i, screenshot in enumerate(screenshots, 1):
                    try:
                        print(f"Uploading {i}/{len(screenshots)}: {screenshot['filename']}")
                        await page.keyboard.press('Control+U')
                        await page.wait_for_timeout(1000)
                        file_inputs = await page.query_selector_all('input[type="file"]')
                        if file_inputs:
                            await file_inputs[0].set_input_files(screenshot['path'])
                            await page.wait_for_timeout(3000)
                    except Exception as e:
                        print(f"   Error: {str(e)[:100]}")

            except Exception as e:
                print(f"Error creating board: {str(e)[:150]}")

        else:
            print(f"\nUnexpected page. Current URL: {current_url}")
            print("Please check the browser window.")

        print("\nBrowser staying open for 60 seconds for manual review/upload...")
        print("You can manually drag and drop the screenshots if needed.")
        print(f"Screenshot files location: {os.getcwd()}")
        await page.wait_for_timeout(60000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
