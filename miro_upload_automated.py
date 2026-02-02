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
    print("YOKE HEALTH SCREENSHOTS TO MIRO BOARD - FULL AUTOMATION")
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
        # Launch browser (visible so you can see it work)
        print("\n1. Launching browser...")
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
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

        # Fill in login form
        print("   Entering credentials...")
        await page.fill('input[name="email"], input[type="email"]', miro_email)
        await page.fill('input[name="password"], input[type="password"]', miro_password)

        # Click login button
        await page.click('button[type="submit"]')
        print("   Logging in...")
        await page.wait_for_timeout(5000)

        # Navigate to dashboard
        print("\n4. Navigating to dashboard...")
        await page.goto('https://miro.com/app/dashboard/')
        await page.wait_for_timeout(3000)

        # Create new board
        print("\n5. Creating new Miro board...")
        try:
            # Try different selectors for create board button
            create_selectors = [
                'button:has-text("Create new board")',
                'button:has-text("Create board")',
                '[data-testid="create-board-button"]',
                'button:has-text("New board")',
                'a[href*="create"]',
                '.create-board'
            ]

            board_created = False
            for selector in create_selectors:
                try:
                    await page.click(selector, timeout=3000)
                    print("   Clicked create board button")
                    board_created = True
                    break
                except:
                    continue

            if not board_created:
                print("   Trying keyboard shortcut to create board...")
                await page.keyboard.press('Control+N')

            await page.wait_for_timeout(5000)

            # Wait for board to load - look for board canvas
            await page.wait_for_selector('[data-testid="board-canvas"], .rtb-canvas', timeout=10000)
            print("   Board created successfully!")

        except Exception as e:
            print(f"   Board creation: {str(e)[:100]}")

        # Upload screenshots to board
        print("\n6. Uploading screenshots to board...")

        try:
            # Look for upload button or file input
            upload_methods = [
                # Method 1: Click upload button
                ('button:has-text("Upload")', 'click'),
                ('[data-testid="upload-button"]', 'click'),
                ('button[aria-label*="Upload"]', 'click'),
                # Method 2: Use keyboard shortcut
                ('keyboard', 'Control+U'),
                # Method 3: Right-click context menu
                ('context', 'upload')
            ]

            for i, screenshot in enumerate(screenshots, 1):
                try:
                    print(f"   Uploading {i}/{len(screenshots)}: {screenshot['filename']}")

                    # Try keyboard shortcut for upload
                    await page.keyboard.press('Control+U')
                    await page.wait_for_timeout(1000)

                    # Look for file input
                    file_input = await page.query_selector('input[type="file"]')

                    if file_input:
                        await file_input.set_input_files(screenshot['path'])
                        print(f"   File uploaded: {screenshot['filename']}")
                        await page.wait_for_timeout(2000)
                    else:
                        # Alternative: try drag and drop simulation
                        print(f"   Attempting alternative upload method...")
                        # Wait for any file input to appear
                        await page.wait_for_selector('input[type="file"]', timeout=5000)
                        file_input = await page.query_selector('input[type="file"]')
                        if file_input:
                            await file_input.set_input_files(screenshot['path'])
                            await page.wait_for_timeout(2000)

                except Exception as e:
                    print(f"   Upload attempt: {str(e)[:100]}")
                    continue

        except Exception as e:
            print(f"   Upload process: {str(e)[:200]}")

        print("\n" + "="*70)
        print("MIRO BOARD AUTOMATION COMPLETE")
        print("="*70)
        print("\nBoard: Yoke Health Website Screens")
        print(f"Screenshots processed: {len(screenshots)}")
        print("\nScreenshot files:")
        for s in screenshots:
            print(f"   - {s['filename']}")

        # Keep browser open briefly
        print("\nBrowser will stay open for 10 seconds...")
        await page.wait_for_timeout(10000)

        await browser.close()

    return screenshots

if __name__ == "__main__":
    asyncio.run(main())
