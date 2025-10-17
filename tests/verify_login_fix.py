from playwright.sync_api import sync_playwright, Page, expect
import os

def test_login_flow(page: Page):
    """
    Tests that the login form appears correctly after selecting a user profile.
    """
    # Listen for all console events and print them to help with debugging.
    page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))

    # Construct the absolute path to the file to avoid ambiguity.
    file_path = os.path.abspath("index.htm")
    page.goto(f"file://{file_path}")

    # 1. Fill in the email and password.
    page.locator("#email").fill("test@test.com")
    page.locator("#password").fill("password")

    # 2. Check the "Lembrar senha" checkbox.
    page.locator("#remember-me").check()

    # 3. Click the "Entrar" button.
    page.get_by_role("button", name="Entrar").click()

    # 4. Assert that the logged-in view is visible.
    logged_in_view = page.locator("#logged-in-app")
    expect(logged_in_view).to_be_visible(timeout=15000)

    # 5. Assert that the email was saved to localStorage.
    saved_email = page.evaluate("localStorage.getItem('rememberedEmail')")
    assert saved_email == "test@test.com"

    # 5. Take a screenshot for visual confirmation.
    os.makedirs("jules-scratch/verification", exist_ok=True)
    page.screenshot(path="jules-scratch/verification/verification.png")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_login_flow(page)
        finally:
            browser.close()

if __name__ == "__main__":
    main()