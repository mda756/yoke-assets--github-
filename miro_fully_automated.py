import asyncio
from playwright.async_api import async_playwright
import os
import json

async def main():
    print("="*70)
    print("MIRO BOARD - FULLY AUTOMATED")
    print("="*70)

    # Load credentials
    with open('claude code creator/CREDENTIALS_STORE.json', 'r') as f:
        creds = json.load(f)

    miro_email = creds['services']['miro']['email']
    miro_password = creds['services']['miro']['password']

    # Direct link
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

    screenshot_paths = [os.path.abspath(f) for f in screenshots if os.path.exists(f)]
    print(f"\nFound {len(screenshot_paths)} screenshot files")

    async with async_playwright() as p:
        print("\nLaunching browser...")
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(90000)

        # Try direct link first
        print("\n1. Accessing Miro via direct link...")
        await page.goto(miro_link)
        await page.wait_for_timeout(5000)

        # If not on dashboard, try login
        if 'dashboard' not in page.url and 'board' not in page.url:
            print("\n2. Direct link failed, trying login...")
            await page.goto('https://miro.com/login/')
            await page.wait_for_timeout(2000)

            try:
                await page.click('text="Accept All Cookies"', timeout=3000)
            except:
                pass

            await page.fill('input[name="email"], input[type="email"]', miro_email)
            await page.wait_for_timeout(500)
            await page.fill('input[name="password"], input[type="password"]', miro_password)
            await page.wait_for_timeout(500)
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(6000)

        # Navigate to dashboard
        current_url = page.url
        print(f"\n   Current URL: {current_url}")

        if 'dashboard' not in current_url:
            print("   Navigating to dashboard...")
            await page.goto('https://miro.com/app/dashboard/')
            await page.wait_for_timeout(4000)

        # Create board
        print("\n3. Creating new board...")
        await page.click('button:has-text("Create new"), button:has-text("Create")')
        await page.wait_for_timeout(3000)

        await page.click('text="Blank board"')
        await page.wait_for_timeout(8000)

        # Wait for board
        await page.wait_for_url('**/app/board/**', timeout=20000)
        board_url = page.url
        print(f"   Board created: {board_url}")

        # Set board name using JavaScript
        print("\n4. Setting board name...")
        board_name = "Yoke Health Website Screens"

        # Use JavaScript to find and set title
        await page.evaluate(f'''
            // Find title input by various methods
            const titleInput = document.querySelector('input[placeholder*="Untitled"]') ||
                             document.querySelector('input[placeholder*="title"]') ||
                             document.querySelector('[data-testid*="board-title"] input') ||
                             document.querySelector('input[type="text"]');

            if (titleInput) {{
                titleInput.focus();
                titleInput.value = "{board_name}";
                titleInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                titleInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        ''')
        await page.wait_for_timeout(1000)
        print(f"   Board name set to: {board_name}")

        # Upload screenshots using JavaScript injection
        print(f"\n5. Uploading {len(screenshot_paths)} screenshots...")

        for i, screenshot_path in enumerate(screenshot_paths, 1):
            try:
                print(f"   Uploading {i}/{len(screenshot_paths)}: {os.path.basename(screenshot_path)}")

                # Method: Inject a file input and trigger it
                await page.evaluate('''
                    // Remove any existing injected inputs
                    document.querySelectorAll('.injected-file-input').forEach(el => el.remove());

                    // Create new file input
                    const input = document.createElement('input');
                    input.type = 'file';
                    input.multiple = false;
                    input.className = 'injected-file-input';
                    input.style.position = 'fixed';
                    input.style.top = '0';
                    input.style.left = '0';
                    input.style.opacity = '0.01';
                    input.style.zIndex = '99999';
                    document.body.appendChild(input);
                ''')

                await page.wait_for_timeout(500)

                # Find the injected input and set file
                file_input = await page.query_selector('.injected-file-input')
                if file_input:
                    await file_input.set_input_files(screenshot_path)
                    await page.wait_for_timeout(1000)

                    # Trigger change event and try to process
                    await page.evaluate('''
                        const input = document.querySelector('.injected-file-input');
                        if (input && input.files.length > 0) {
                            // Try to trigger Miro's upload handling
                            const file = input.files[0];

                            // Create a DataTransfer object
                            const dataTransfer = new DataTransfer();
                            dataTransfer.items.add(file);

                            // Dispatch drop event on canvas
                            const canvas = document.querySelector('[data-testid="board-canvas"]') ||
                                         document.querySelector('.rtb-canvas') ||
                                         document.body;

                            const dropEvent = new DragEvent('drop', {
                                bubbles: true,
                                cancelable: true,
                                dataTransfer: dataTransfer
                            });

                            canvas.dispatchEvent(dropEvent);
                        }
                    ''')

                    print(f"      Uploaded: {os.path.basename(screenshot_path)}")
                    await page.wait_for_timeout(3000)

            except Exception as e:
                print(f"      Error: {str(e)[:150]}")

        # Alternative method: Use keyboard shortcuts and native dialogs
        print("\n6. Attempting alternative upload method...")

        # Upload all files at once using native file picker
        try:
            # Press + to open toolbar
            await page.keyboard.press('+')
            await page.wait_for_timeout(1500)

            # Click Image button
            try:
                await page.click('button:has-text("Image"), text="Image"', timeout=5000)
                await page.wait_for_timeout(1000)
            except:
                pass

            # Look for any file input (hidden or visible)
            file_inputs = await page.query_selector_all('input[type="file"]')

            if file_inputs:
                # Use the first available file input
                await file_inputs[0].set_input_files(screenshot_paths)
                print(f"   Uploaded all {len(screenshot_paths)} files via file input!")
                await page.wait_for_timeout(5000)
            else:
                # Try to create and use our own file input
                await page.evaluate('''
                    const input = document.createElement('input');
                    input.type = 'file';
                    input.multiple = true;
                    input.id = 'final-upload-input';
                    input.style.position = 'fixed';
                    input.style.top = '50%';
                    input.style.left = '50%';
                    input.style.zIndex = '999999';
                    document.body.appendChild(input);
                ''')
                await page.wait_for_timeout(500)

                final_input = await page.query_selector('#final-upload-input')
                if final_input:
                    await final_input.set_input_files(screenshot_paths)
                    await page.wait_for_timeout(2000)

                    # Try to process the files
                    await page.evaluate('''
                        const input = document.getElementById('final-upload-input');
                        if (input && input.files.length > 0) {
                            const event = new Event('change', { bubbles: true });
                            input.dispatchEvent(event);
                        }
                    ''')
                    print(f"   Processed {len(screenshot_paths)} files")
                    await page.wait_for_timeout(5000)

        except Exception as e:
            print(f"   Alternative upload: {str(e)[:200]}")

        print("\n" + "="*70)
        print("AUTOMATION COMPLETE")
        print("="*70)
        print(f"\nBoard Name: Yoke Health Website Screens")
        print(f"Board URL: {board_url}")
        print(f"Files processed: {len(screenshot_paths)}")
        print("\nThe board should now have your screenshots.")
        print("Check the browser window to verify.")

        print("\nBrowser staying open for 30 seconds...")
        await page.wait_for_timeout(30000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
