import asyncio
from playwright.async_api import async_playwright
import os
import json

async def main():
    print("="*70)
    print("MIRO UPLOAD - TOOLBAR ICON METHOD")
    print("="*70)

    screenshot_name = "nexgenhc_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)
    auth_file = "miro_auth_state.json"

    if not os.path.exists(screenshot_name):
        print("ERROR: Screenshot not found")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=700)

        with open(auth_file, 'r') as f:
            storage_state = json.load(f)

        context = await browser.new_context(storage_state=storage_state)
        page = await context.new_page()
        page.set_default_timeout(120000)

        # Create board
        print("\nCreating board...")
        await page.goto('https://miro.com/app/dashboard/')
        await page.wait_for_timeout(4000)

        await page.click('button:has-text("Create new"), button:has-text("Create")')
        await page.wait_for_timeout(3000)

        await page.click('text="Blank board"')
        await page.wait_for_timeout(8000)

        await page.wait_for_url('**/app/board/**', timeout=20000)
        board_url = page.url
        print(f"Board created: {board_url}")

        await page.wait_for_timeout(3000)

        # Close ALL dialogs/popups
        print("\nClosing all dialogs...")
        # Try ESC key to close dialogs
        await page.keyboard.press('Escape')
        await page.wait_for_timeout(1000)
        await page.keyboard.press('Escape')
        await page.wait_for_timeout(1000)

        # Click on board canvas to focus it
        print("Focusing board canvas...")
        try:
            await page.click('[data-testid="board-canvas"]', position={'x': 400, 'y': 300}, timeout=3000)
        except:
            await page.click('body', position={'x': 400, 'y': 300})

        await page.wait_for_timeout(2000)

        # Try right-click context menu
        print("\nTrying right-click context menu...")
        await page.click('body', button='right', position={'x': 640, 'y': 400})
        await page.wait_for_timeout(2000)

        # Look for Upload or Image option in context menu
        try:
            await page.click('text="Upload"', timeout=3000)
            print("  Clicked Upload from context menu")
        except:
            try:
                await page.click('text="Image"', timeout=3000)
                print("  Clicked Image from context menu")
            except:
                print("  No Upload/Image in context menu")

        await page.wait_for_timeout(2000)

        # Check for file inputs
        file_inputs = await page.query_selector_all('input[type="file"]')
        print(f"\nFile inputs: {len(file_inputs)}")

        if file_inputs:
            print("Uploading...")
            await file_inputs[-1].set_input_files(screenshot_path)
            print("Uploaded!")
            await page.wait_for_timeout(15000)

            print("\n" + "="*70)
            print("SUCCESS!")
            print("="*70)
            print(f"Board: {board_url}")

        else:
            # Try drag and drop simulation
            print("\nTrying drag-drop simulation...")
            await page.evaluate(f'''
                const file = new File(["dummy"], "nexgenhc_homepage.png", {{ type: "image/png" }});
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);

                const dropEvent = new DragEvent('drop', {{
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dataTransfer
                }});

                document.body.dispatchEvent(dropEvent);
            ''')
            print("Drag-drop event dispatched")
            await page.wait_for_timeout(3000)

            # Check again for file inputs
            file_inputs = await page.query_selector_all('input[type="file"]')
            if file_inputs:
                await file_inputs[-1].set_input_files(screenshot_path)
                print("Uploaded via drag-drop trigger!")
                await page.wait_for_timeout(15000)

        await page.screenshot(path='miro_final_state.png')
        print("\nFinal state screenshot: miro_final_state.png")

        print("\nBrowser open for 60 seconds...")
        await page.wait_for_timeout(60000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
