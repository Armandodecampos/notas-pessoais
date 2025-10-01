from playwright.sync_api import sync_playwright, expect
import os

def run_verification(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Get the absolute path to the HTML file
        file_path = os.path.abspath('index.htm')
        page.goto(f'file://{file_path}')

        # 1. Simulate login by directly showing the logged-in view
        page.evaluate("""() => {
            document.getElementById('main-container').classList.add('hidden');
            document.getElementById('logged-in-app').classList.remove('hidden');
        }""")

        # 2. Open the app options modal
        # Wait for the button grid to be populated, which now should be visible
        expect(page.locator("#button-grid-container .app-container").first).to_be_visible(timeout=10000)

        # 3. Verify the changes in the modal
        # Directly show the modal to bypass click event dependencies
        page.evaluate("""() => {
            const modal = document.getElementById('app-options-modal');
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }""")

        # Wait for the modal to appear
        app_options_modal = page.locator("#app-options-modal")
        expect(app_options_modal).to_be_visible(timeout=10000)

        # Assert that the close 'X' button in the header is NOT visible
        close_button_header = app_options_modal.locator("header button")
        expect(close_button_header).not_to_be_visible()

        # Take a screenshot of the modal
        page.screenshot(path="jules-scratch/verification/verification.png")

        print("Verification script ran successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)