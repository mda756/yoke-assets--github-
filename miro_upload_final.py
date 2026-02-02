import asyncio
from playwright.async_api import async_playwright
import json
import os

async def scroll_to_bottom(page):
    """Scroll to bottom to trigger lazy loading"""
    page_height = await page.evaluate('document.body.scrollHeight')
    viewport_height = await page.evaluate('window.innerHeight')
    current_position = 0
    scroll_step = viewport_height

    while current_position < page_height:
        await page.evaluate(f'window.scrollTo(0, {current_position})')
        await page.wait_for_timeout(500)
        current_position += scroll_step
        new_height = await page.evaluate('document.body.scrollHeight')
        if new_height > page_height:
            page_height = new_height

    await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    await page.wait_for_timeout(1000)
    await page.evaluate('window.scrollTo(0, 0)')
    await page.wait_for_timeout(500)

async def main():
    print("="*70)
    print("YOKE HEALTH TO MIRO - FINAL AUTOMATION")
    print("="*70)

    # Load credentials
    with open('claude code creator/CREDENTIALS_STORE.json', 'r') as f:
        creds = json.load(f)

    miro_email = creds['services']['miro']['email']
    miro_password = creds['services']['miro']['password']

    # Pages to capture
    pages_to_capture = [
        {"name": "Home", "url": "https://yokehealth.com"},
        {"name": "AI Healthcare Platforms", "url": "https://yokehealth.com/ai-healthcare-platform-2/"},
        {"name": "Our Work", "url": "https://yokehealth.com/case-studies-digital-pharma-healthcare/"},
        {"name": "Agency", "url": "https://yokehealth.com/agency-services/"},
        {"name": "Biotech", "url": "https://yokehealth.com/biotechs/"},
        {"name": "Team", "url": "https://yokehealth.com/your-team/"},
        {"name": "Contact", "url": "https://yokehealth.com/contact-us/"},
    ]

    screenshots = []

    async with async_playwright() as p:
        # Launch browser
        print("\n1. Launching browser...")
        browser = await p.chromium.launch(headless=False, slow_mo=800)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(90000)

        # Capture screenshots
        print("\n2. Capturing Yoke Health screenshots...")
        for i, page_info in enumerate(pages_to_capture, 1):
            try:
                print(f"\n   [{i}/{len(pages_to_capture)}] {page_info['name']}")
                await page.goto(page_info['url'], wait_until="networkidle")
                await page.wait_for_timeout(2000)
                await scroll_to_bottom(page)

                screenshot_name = f"yoke_{i}_{page_info['name'].replace(' ', '_')}.png"
                screenshot_path = os.path.abspath(screenshot_name)
                await page.screenshot(path=screenshot_name, full_page=True)
                print(f"   Screenshot saved: {screenshot_name}")

                screenshots.append({
                    'name': page_info['name'],
                    'path': screenshot_path,
                    'filename': screenshot_name
                })

            except Exception as e:
                print(f"   ERROR: {str(e)[:100]}")

        # Login to Miro
        print("\n3. Logging into Miro...")
        await page.goto('https://miro.com/login/')
        await page.wait_for_timeout(2000)

        # Accept cookies if present
        try:
            await page.click('text="Accept All Cookies"', timeout=3000)
        except:
            pass

        # Fill in login form
        print("   Entering credentials...")
        await page.fill('input[name="email"], input[type="email"]', miro_email)
        await page.wait_for_timeout(500)
        await page.fill('input[name="password"], input[type="password"]', miro_password)
        await page.wait_for_timeout(500)

        # Click login button
        await page.click('button[type="submit"]')
        print("   Logging in...")
        await page.wait_for_timeout(6000)

        # Wait for dashboard to load
        try:
            await page.wait_for_url('**/app/dashboard/**', timeout=10000)
            print("   Successfully logged in!")
        except:
            print("   Checking if login was successful...")
            current_url = page.url
            print(f"   Current URL: {current_url}")

        # Navigate to dashboard if not there
        if 'dashboard' not in page.url:
            print("   Navigating to dashboard...")
            await page.goto('https://miro.com/app/dashboard/')
            await page.wait_for_timeout(3000)

        # Create new board
        print("\n4. Creating new Miro board...")
        await page.wait_for_timeout(2000)

        try:
            # Click "Create new" button
            await page.click('button:has-text("Create new"), button:has-text("Create")', timeout=5000)
            print("   Clicked Create new button")
            await page.wait_for_timeout(2000)

            # Click "Blank board"
            await page.click('text="Blank board"', timeout=5000)
            print("   Selected Blank board")
            await page.wait_for_timeout(5000)

            # Wait for board to load
            await page.wait_for_url('**/app/board/**', timeout=15000)
            print("   Board created successfully!")

            # Set board name
            print("   Setting board name...")
            # Try to find and click the board name field
            try:
                # Look for board title input
                title_selectors = [
                    'input[placeholder*="Board title"]',
                    'input[placeholder*="Untitled"]',
                    '[data-testid="board-title-input"]',
                    'input[type="text"][value="Untitled"]'
                ]

                for selector in title_selectors:
                    try:
                        await page.click(selector, timeout=2000)
                        await page.fill(selector, "Yoke Health Website Screens")
                        await page.keyboard.press('Enter')
                        print("   Board named: Yoke Health Website Screens")
                        break
                    except:
                        continue

            except Exception as e:
                print(f"   Could not set board name: {str(e)[:100]}")

            await page.wait_for_timeout(2000)

        except Exception as e:
            print(f"   Board creation issue: {str(e)[:150]}")

        # Upload screenshots to board
        print("\n5. Uploading screenshots to board...")

        # Get current board URL for reference
        board_url = page.url
        print(f"   Board URL: {board_url}")

        for i, screenshot in enumerate(screenshots, 1):
            try:
                print(f"\n   Uploading {i}/{len(screenshots)}: {screenshot['filename']}")

                # Method 1: Try file input (check if any exist)
                file_inputs = await page.query_selector_all('input[type="file"]')

                if not file_inputs:
                    # Try to trigger upload dialog using keyboard or click
                    try:
                        # Try Ctrl+U shortcut
                        await page.keyboard.press('Control+U')
                        await page.wait_for_timeout(1000)
                        file_inputs = await page.query_selector_all('input[type="file"]')
                    except:
                        pass

                if file_inputs:
                    # Upload via file input
                    await file_inputs[0].set_input_files(screenshot['path'])
                    print(f"   Uploaded: {screenshot['filename']}")
                    await page.wait_for_timeout(3000)
                else:
                    print(f"   Could not find upload method for: {screenshot['filename']}")

            except Exception as e:
                print(f"   Upload error: {str(e)[:150]}")

        print("\n" + "="*70)
        print("PROCESS COMPLETE")
        print("="*70)
        print("\nBoard created: Yoke Health Website Screens")
        print(f"Board URL: {board_url}")
        print(f"\nScreenshots captured: {len(screenshots)}")
        print("\nNote: If uploads failed, you can manually drag the files to the board.")
        print("Screenshot files are in:", os.getcwd())

        # Keep browser open
        print("\nBrowser will stay open for 30 seconds for review...")
        await page.wait_for_timeout(30000)

        await browser.close()

    return screenshots

if __name__ == "__main__":
    asyncio.run(main())
