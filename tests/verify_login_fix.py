from playwright.sync_api import sync_playwright, Page, expect
import os
import http.server
import socketserver
import threading
import time

PORT = 8080

def test_login_success(page: Page):
    """
    Tests that the login is successful, reloading the page to ensure UI updates.
    """
    page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))

    page.goto(f"http://localhost:{PORT}/index.htm", wait_until="networkidle")

    page.locator("#email").fill("test@test.com")
    page.locator("#password").fill("123456")

    login_button = page.get_by_role("button", name="Entrar")
    expect(login_button).to_be_visible()
    login_button.click()

    # Recarrega a página para garantir que o onAuthStateChange seja acionado
    page.reload(wait_until="networkidle")

    logged_in_view = page.locator("#logged-in-app")
    expect(logged_in_view).to_be_visible(timeout=30000)

def main():
    socketserver.TCPServer.allow_reuse_address = True
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print(f"Serving on port {PORT}")
    time.sleep(1)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                test_login_success(page)
                print("Test passed: Login is successful.")
            finally:
                browser.close()
    finally:
        print("Stopping server...")
        httpd.shutdown()
        httpd.server_close()
        server_thread.join()

if __name__ == "__main__":
    main()
