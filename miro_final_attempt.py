import asyncio
from playwright.async_api import async_playwright
import os
import json

async def main():
    print("="*70)
    print("MIRO - FINAL AUTOMATED ATTEMPT")
    print("="*70)

    screenshot_name = "nexgenhc_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)
    auth_file = "miro_auth_state.json"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=600)

        with open(auth_file, 'r') as f:
            storage_state = json.load(f)

        context = await browser.new_context(storage_state=storage_state)
        page = await context.new_page()
        page.set_default_timeout(120000)

        # Create board
        print("\nCreating board...")
        await page.goto('https://miro.com/app/dashboard/')
        await page.wait_for_timeout(4000)

        await page.click('button:has-text("Create new")')
        await page.wait_for_timeout(3000)

        await page.click('text="Blank board"')
        await page.wait_for_timeout(8000)

        await page.wait_for_url('**/app/board/**', timeout=20000)
        board_url = page.url
        print(f"Board: {board_url}")

        await page.wait_for_timeout(3000)

        # Close popup at coordinates
        print("Closing popup...")
        await page.mouse.click(987, 191)
        await page.wait_for_timeout(2000)

        # Try menu bar at top - File, Edit, Insert, etc
        print("\nTrying menu bar...")
        menu_options = ['Insert', 'File', 'View']
        for menu in menu_options:
            try:
                await page.click(f'text="{menu}"', timeout=2000)
                await page.wait_for_timeout(1000)

                # Look for Upload/Image option
                try:
                    await page.click('text="Upload"', timeout=2000)
                    print(f"  Found Upload in {menu} menu")
                    break
                except:
                    try:
                        await page.click('text="Image"', timeout=2000)
                        print(f"  Found Image in {menu} menu")
                        break
                    except:
                        await page.keyboard.press('Escape')
            except:
                continue

        await page.wait_for_timeout(2000)

        # Check for file inputs
        file_inputs = await page.query_selector_all('input[type="file"]')

        if not file_inputs:
            # Try clicking each toolbar icon systematically
            print("\nTrying toolbar icons...")

            # Get all clickable elements in the left toolbar
            toolbar = await page.query_selector('.rtb-left-toolbar, [data-testid="left-toolbar"]')
            if toolbar:
                buttons = await toolbar.query_selector_all('button')
                print(f"  Found {len(buttons)} toolbar buttons")

                for i, button in enumerate(buttons):
                    try:
                        await button.click()
                        print(f"  Clicked button {i+1}")
                        await page.wait_for_timeout(1500)

                        # Check if file input appeared
                        file_inputs = await page.query_selector_all('input[type="file"]')
                        if file_inputs:
                            print(f"  File input appeared after button {i+1}!")
                            break

                    except:
                        continue

        # If still no file input, try drag-drop with actual file
        if not file_inputs:
            print("\nTrying actual file drag-drop...")

            # Create a data transfer with the actual file
            await page.evaluate(f'''
                async () => {{
                    const response = await fetch('file:///{screenshot_path.replace(chr(92), '/')}');
                    const blob = await response.blob();
                    const file = new File([blob], "{screenshot_name}", {{ type: "image/png" }});

                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);

                    const canvas = document.querySelector('[data-testid="board-canvas"]') || document.body;
                    const dropEvent = new DragEvent('drop', {{
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dataTransfer
                    }});

                    canvas.dispatchEvent(dropEvent);
                }}
            ''')

            await page.wait_for_timeout(3000)
            file_inputs = await page.query_selector_all('input[type="file"]')

        # Upload if file input found
        if file_inputs:
            print("\nUploading file...")
            await file_inputs[-1].set_input_files(screenshot_path)
            print("FILE UPLOADED!")
            await page.wait_for_timeout(15000)

            print("\n" + "="*70)
            print("SUCCESS!")
            print("="*70)
            print(f"Board: nexgenhc home screen")
            print(f"URL: {board_url}")
        else:
            print("\nCould not trigger file upload")
            print(f"Board URL: {board_url}")
            print("You can manually upload by dragging the file to the board")

        await page.screenshot(path='final_attempt_result.png')
        print("\nResult screenshot: final_attempt_result.png")

        print("\nBrowser open for 30 seconds...")
        await page.wait_for_timeout(30000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
