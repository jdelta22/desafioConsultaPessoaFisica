import asyncio
import base64

from playwright.async_api import async_playwright


async def realizar_busca(termo_busca):
    async def organizar_resultados(tabelas):

        resultados = []

        total_tabelas = await tabelas.count()

        for i in range(total_tabelas):
            tabela = tabelas.nth(i)

            beneficio = (await tabela.locator("strong").inner_text()).strip()

            linhas = tabela.locator("tbody tr")

            total_linhas = await linhas.count()

            for j in range(total_linhas):
                linha = linhas.nth(j)

                colunas = linha.locator("td")

                nis = (await colunas.nth(1).inner_text()).strip()
                nome = (await colunas.nth(2).inner_text()).strip()
                valor = (await colunas.nth(3).inner_text()).strip()

                link_detalhe = await colunas.nth(0).locator("a").get_attribute("href")

                url_detalhe = "https://portaldatransparencia.gov.br" + link_detalhe

                resultados.append(
                    {
                        "beneficio": beneficio,
                        "nis": nis,
                        "nome": nome,
                        "valor": valor,
                        "url_detalhe": url_detalhe,
                    }
                )

        return resultados

    async def extrair_detalhes(page):

        detalhes = []

        try:
            await page.wait_for_selector(".dados-detalhados", timeout=5000)
        except:
            return detalhes, None

        try:
            await page.locator("#accept-all-btn").click(timeout=3000)
        except:
            pass

        imagem_detalhe = await imagem64(page)

        try:
            await page.locator("#btnPaginacaoCompleta").click(timeout=2000)
            await page.wait_for_timeout(1500)
        except:
            pass

        while True:
            tabelas = page.locator(".dados-detalhados table")

            total_tabelas = await tabelas.count()

            for i in range(total_tabelas):
                tabela = tabelas.nth(i)

                headers = await tabela.locator("thead th").all_inner_texts()

                linhas = tabela.locator("tbody tr")

                total_linhas = await linhas.count()

                for j in range(total_linhas):
                    linha = linhas.nth(j)

                    valores = await linha.locator("td").all_inner_texts()

                    registro = dict(zip(headers, valores))

                    detalhes.append(registro)

            botao_next = page.locator(".paginate_button.next").first

            if await botao_next.count() == 0:
                break

            classes = await botao_next.get_attribute("class")

            if classes and "disabled" in classes:
                break

            await botao_next.click()

            await page.wait_for_timeout(1200)

        return detalhes, imagem_detalhe

    async def imagem64(page):

        screenshot_bytes = await page.screenshot()

        return base64.b64encode(screenshot_bytes).decode()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
            ],
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
        )

        page = await context.new_page()

        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """)

        await page.goto(
            "https://portaldatransparencia.gov.br/pessoa/visao-geral",
            wait_until="domcontentloaded",
        )

        await page.wait_for_load_state("networkidle")

        await page.locator("#link-consulta-pessoa-fisica").click()

        await page.fill("#termo", termo_busca)

        await page.click(
            "//*[@id='form-superior']/section[1]/div/div/fieldset/div/button"
        )

        try:
            await page.locator(".link-busca-nome").first.click()
        except:
            print("Nenhum resultado encontrado.")
            return []

        await page.locator("button.header").click()

        tabelas = page.locator(".box-ficha__resultados .br-table")

        dados = await organizar_resultados(tabelas)

        try:
            await page.locator("#accept-all-btn").click(timeout=3000)
        except:
            pass
        await page.evaluate("""
        document.querySelectorAll('.br-accordion .header')
        .forEach(btn => btn.click())
        """)

        await page.wait_for_timeout(800)
        imagem_resultado = await imagem64(page)

        abas = []

        for item in dados:
            nova_aba = await context.new_page()
            await nova_aba.goto(item["url_detalhe"], wait_until="domcontentloaded")
            abas.append((item, nova_aba))

        for item, aba in abas:
            detalhes, imagem_detalhe = await extrair_detalhes(aba)
            item["detalhes"] = detalhes
            item["imagem_detalhe"] = imagem_detalhe
            await aba.close()

        await browser.close()

        return {"imagem_resultado": imagem_resultado, "resultados": dados}


if __name__ == "__main__":
    termo_busca = input("Digite o nome completo,CPF ou NIS da pessoa física: ")
    print("Iniciando a busca...")
    dados = asyncio.run(realizar_busca(termo_busca))
    print("Organizando resultados...")
    print(dados)
