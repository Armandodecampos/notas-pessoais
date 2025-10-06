from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Navigate to the local HTML file
    import os
    page.goto(f"file://{os.getcwd()}/index.htm")

    # Click the button to show the user profiles
    page.click("#show-profiles-button")

    # Wait for the user list container to be visible
    page.wait_for_selector("#user-list-container:not(.hidden)")

    # Wait for the user list to be populated by looking for the data-email attribute
    page.wait_for_selector("button[data-email]")

    # Take a screenshot
    page.screenshot(path="jules-scratch/verification/verification.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)