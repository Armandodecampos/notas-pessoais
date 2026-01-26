from playwright.sync_api import sync_playwright, Page, expect
import os
import http.server
import socketserver
import threading
import time

PORT = 8080

def test_login_flow(page: Page):
    """
    Tests the complete login flow, waiting for Supabase to initialize.
    """
    page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))

    page.goto(f"http://localhost:{PORT}/index.htm")

    # Espera que o Supabase seja carregado antes de interagir com a página
    page.wait_for_function("() => window.supabase !== undefined")

    page.locator("#email").fill("test@test.com")
    page.locator("#password").fill("password")

    login_button = page.get_by_role("button", name="Entrar")
    expect(login_button).to_be_visible()
    login_button.click()

    logged_in_view = page.locator("#logged-in-app")
    expect(logged_in_view).to_be_visible(timeout=30000)

    os.makedirs("jules-scratch/verification", exist_ok=True)
    page.screenshot(path="jules-scratch/verification/verification.png")

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
                test_login_flow(page)
                print("Test passed successfully!")
            finally:
                browser.close()
    finally:
        print("Stopping server...")
        httpd.shutdown()
        httpd.server_close()
        server_thread.join()

if __name__ == "__main__":
    main()
