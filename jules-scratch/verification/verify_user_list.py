from playwright.sync_api import sync_playwright, Page, expect
import os

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Get the absolute path to the HTML file
    file_path = os.path.abspath('index.htm')

    # Go to the local HTML file
    page.goto(f'file://{file_path}')

    # Click the "Acessar" button to show the user profiles
    page.locator("#show-profiles-button").click()

    # Wait for the user list to be visible
    expect(page.locator("#user-list-container")).to_be_visible()

    # Wait for the user cards to be populated
    page.wait_for_selector(".user-card")

    # Add a static delay to ensure images have time to load
    page.wait_for_timeout(2000)

    # Take a screenshot of the user list
    page.screenshot(path="jules-scratch/verification/verification.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)