import asyncio
import base64


async def realizar_busca(browser, termo_busca):

    async def imagem64(page):
        # Tenta tirar um print da página, mas se der erro (ex: canvas ou conteúdo protegido), retorna None
        try:
            screenshot_bytes = await page.screenshot()
            return base64.b64encode(screenshot_bytes).decode()
        except:
            return None

    async def organizar_resultados(tabelas):
        # recolhe os dados contendo os benficios recebidos e organiza em uma lista de dicionários
        # tambem retorna o url do detalhe para cada beneficio
        resultados = []
        total_tabelas = await tabelas.count()
        for i in range(total_tabelas):
            tabela = tabelas.nth(i)
            try:
                beneficio = (await tabela.locator("strong").inner_text()).strip()
                linhas = tabela.locator("tbody tr")
                total_linhas = await linhas.count()
                for j in range(total_linhas):
                    linha = linhas.nth(j)
                    colunas = linha.locator("td")
                    nis = (await colunas.nth(1).inner_text()).strip()
                    nome = (await colunas.nth(2).inner_text()).strip()
                    valor = (await colunas.nth(3).inner_text()).strip()
                    link_detalhe = (
                        await colunas.nth(0).locator("a").get_attribute("href")
                    )
                    resultados.append(
                        {
                            "beneficio": beneficio,
                            "nis": nis,
                            "nome": nome,
                            "valor": valor,
                            "url_detalhe": f"https://portaldatransparencia.gov.br{link_detalhe}",
                        }
                    )
            except Exception as e:
                print(f"Erro ao organizar linha: {e}")
                continue
        return resultados

    async def extrair_detalhes(page):
        # acessa cada detalhe de beneficio e extrai os dados da tabela paginada, retornando uma lista de dicionarios e a imagem do detalhe (ou None)
        detalhes = []
        try:
            await page.wait_for_selector(".dados-detalhados", timeout=5000)
            try:
                await page.locator("#accept-all-btn").click(timeout=2000)
            except:
                pass

            img_detalhe = await imagem64(page)

            try:
                await page.locator("#btnPaginacaoCompleta").click(timeout=2000)
                await asyncio.sleep(1)
            except:
                pass

            while True:
                tabelas = page.locator(".dados-detalhados table")
                for i in range(await tabelas.count()):
                    tabela = tabelas.nth(i)
                    headers = await tabela.locator("thead th").all_inner_texts()
                    linhas = tabela.locator("tbody tr")
                    for j in range(await linhas.count()):
                        valores = await linhas.nth(j).locator("td").all_inner_texts()
                        detalhes.append(dict(zip(headers, valores)))

                botao_next = page.locator(".paginate_button.next").first
                if await botao_next.count() == 0 or "disabled" in (
                    await botao_next.get_attribute("class") or ""
                ):
                    break
                await botao_next.click()
                await asyncio.sleep(1)

            return detalhes, img_detalhe
        except:
            return [], None

    # navegação inicial e busca por termo utilizado.
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
    )

    try:
        page = await context.new_page()
        await page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

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
            await page.locator(".link-busca-nome").first.wait_for(timeout=6000)
            await page.locator(".link-busca-nome").first.click()
        except:
            return []

        await page.locator("button.header").click()
        tabelas = page.locator(".box-ficha__resultados .br-table")
        dados = await organizar_resultados(tabelas)

        await page.evaluate(
            "document.querySelectorAll('.br-accordion .header').forEach(btn => btn.click())"
        )
        await asyncio.sleep(1)
        imagem_resultado = await imagem64(page)

        # Extração de detalhes (Processando um por um)
        for item in dados:
            aba_detalhe = await context.new_page()
            try:
                await aba_detalhe.goto(
                    item["url_detalhe"], wait_until="domcontentloaded"
                )
                detalhes, img_detalhe = await extrair_detalhes(aba_detalhe)
                item["detalhes"] = detalhes
                item["imagem_detalhe"] = img_detalhe
            finally:
                await aba_detalhe.close()

        return {"imagem_resultado": imagem_resultado, "resultados": dados}

    except Exception as e:
        print(f"Erro na busca: {e}")
        return []
    finally:
        # Fecha o contexto e todas as abas vinculadas a ele
        await context.close()
