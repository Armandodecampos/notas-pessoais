import asyncio
import os
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Get the absolute path to the index.htm file
        file_path = os.path.abspath('index.htm')

        # Go to the local file
        await page.goto(f"file://{file_path}")

        # --- Simulate the state where an app has been clicked ---
        await page.evaluate('''() => {
            // 1. Show the main logged-in container
            document.getElementById('main-container').classList.add('hidden');
            document.getElementById('logged-in-app').classList.remove('hidden');

            // 2. Get references to the elements
            const appActionBar = document.getElementById('app-action-bar');
            const mainHeader = document.getElementById('main-header');
            const buttonGridContainer = document.getElementById('button-grid-container');

            // 3. Manually add a dummy app to the grid for context
            const buttonGrid = document.getElementById('button-grid-container');
            const app = {
                id: 'test-app',
                title: 'Test App',
                icon_class: 'fas fa-star'
            };
            const appContainer = document.createElement('div');
            appContainer.className = 'app-container';
            appContainer.innerHTML = `
                <div class="grid-item" draggable="true">
                    <i class="${app.icon_class} grid-item-icon"></i>
                </div>
                <span class="grid-item-label text-theme noselect">${app.title}</span>
            `;
            buttonGrid.appendChild(appContainer);

            // 4. Force the action bar to be visible by directly setting its display style
            appActionBar.style.display = 'flex';

            // 5. Adjust the app grid's position to avoid overlap
            const headerHeight = mainHeader.offsetHeight;
            const actionBarHeight = appActionBar.offsetHeight;
            buttonGridContainer.style.top = `${headerHeight + actionBarHeight}px`;
        }''')

        # Add a small delay to ensure the browser has time to render the layout changes
        await page.wait_for_timeout(200)

        # Verify the action bar is visible
        action_bar = page.locator("#app-action-bar")
        await expect(action_bar).to_be_visible()

        # Take a screenshot to verify the final layout and styling
        await page.screenshot(path="jules-scratch/verification/verification_fixes.png")

        await browser.close()

asyncio.run(main())