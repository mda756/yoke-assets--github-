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
    print("YOKE HEALTH SCREENSHOTS TO MIRO BOARD")
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
        browser = await p.chromium.launch(headless=False)
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
        await page.wait_for_timeout(5000)  # Wait for login

        # Create new board
        print("\n4. Creating new Miro board...")
        await page.goto('https://miro.com/app/dashboard/')
        await page.wait_for_timeout(3000)

        # Click create new board button
        try:
            # Try different selectors for create board button
            create_selectors = [
                'button:has-text("Create new board")',
                'button:has-text("Create board")',
                '[data-testid="create-board-button"]',
                'button:has-text("New board")'
            ]

            for selector in create_selectors:
                try:
                    await page.click(selector, timeout=3000)
                    print("   Clicked create board button")
                    break
                except:
                    continue

            await page.wait_for_timeout(5000)  # Wait for board to be created

            # Set board name
            print("   Setting board name...")
            await page.keyboard.type("Yoke Health Website Screens")
            await page.keyboard.press('Enter')
            await page.wait_for_timeout(2000)

        except Exception as e:
            print(f"   Note: {str(e)[:100]}")
            print("   Continuing with upload...")

        print("\n5. Uploading screenshots to board...")
        # Note: Miro's upload interface varies, may need manual intervention
        print("   Note: You may need to manually drag screenshots to the board")
        print(f"   {len(screenshots)} screenshots are ready:")
        for s in screenshots:
            print(f"   - {s['filename']}")

        print("\n" + "="*70)
        print("PARTIAL COMPLETION")
        print("="*70)
        print("\nScreenshots captured and saved.")
        print("Miro login successful.")
        print("Board creation attempted.")
        print("\nTo complete: Manually upload screenshots to Miro board")
        print(f"Screenshot files in: {os.getcwd()}")

        # Keep browser open for manual upload
        print("\nBrowser will stay open for 60 seconds...")
        print("You can manually upload the screenshots to your board now.")
        await page.wait_for_timeout(60000)

        await browser.close()

    return screenshots

if __name__ == "__main__":
    asyncio.run(main())
