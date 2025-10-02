import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Obter o caminho absoluto do arquivo
        import os
        file_path = os.path.abspath('index.htm')

        await page.goto(f'file://{file_path}')

        # Simulate the logged-in state by showing the correct container
        await page.evaluate('''() => {
            document.getElementById('logged-in-app').classList.remove('hidden');
            document.getElementById('main-container').classList.add('hidden');
        }''')

        # Define dummy data and call the exposed renderApps function
        dummy_apps = [
            { "id": "shopping-list", "title": "Compras", "icon_class": "fas fa-shopping-cart", "isFixed": True },
            { "id": "notes-app", "title": "Notas", "icon_class": "fas fa-sticky-note", "isFixed": True },
            { "id": "recipes-app", "title": "Receitas", "icon_class": "fas fa-utensils", "isFixed": True }
        ]
        dummy_order = ["shopping-list", "notes-app", "recipes-app"]

        await page.evaluate(
            "([apps, order]) => window.renderApps(apps, order)", [dummy_apps, dummy_order]
        )

        # Aguarda o carregamento dos aplicativos
        await page.wait_for_selector('.app-container')

        # Pega o primeiro aplicativo da lista
        first_app_container = page.locator('.app-container').first

        # Clica no primeiro aplicativo para mostrar os botões
        await first_app_container.click()

        # Pega o contêiner de ações associado
        actions_container = first_app_container.locator('..').locator('.app-actions')

        # Verifica se os botões estão visíveis
        await expect(actions_container).to_be_visible()
        await expect(actions_container.get_by_text('Abrir')).to_be_visible()
        await expect(actions_container.get_by_text('Editar')).to_be_visible()
        await expect(actions_container.get_by_text('Remover')).to_be_visible()

        # Tira a primeira screenshot
        await page.screenshot(path="jules-scratch/verification/01_buttons_visible.png")

        # Aguarda 6 segundos para garantir que o timer escondeu os botões
        await asyncio.sleep(6)

        # Verifica se os botões desapareceram
        await expect(actions_container).to_be_hidden()

        # Tira a segunda screenshot
        await page.screenshot(path="jules-scratch/verification/02_buttons_hidden_after_timer.png")

        await browser.close()

asyncio.run(main())