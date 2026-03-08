import asyncio
import uuid
from contextlib import asynccontextmanager
from datetime import datetime

import pytz
from fastapi import FastAPI
from playwright.async_api import async_playwright

from scraper import realizar_busca

# Configuração de Fuso Horário
br_timezone = pytz.timezone("America/Sao_Paulo")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicia o Playwright e o Browser uma única vez no boot da API
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"],
    )
    app.state.browser = browser
    app.state.playwright = playwright

    yield

    # Fecha tudo ao desligar o servidor
    await browser.close()
    await playwright.stop()


app = FastAPI(lifespan=lifespan)

# Limita a 3 buscas simultâneas para não ser bloqueado por IP ou estourar RAM
sem = asyncio.Semaphore(3)


def gerar_id_consulta():
    # id aleatorio
    uid = uuid.uuid4().hex[:8]
    timestamp = datetime.now(br_timezone).strftime("%Y%m%d_%H%M%S")
    return f"{uid}_{timestamp}"


@app.get("/consulta/{termo}")
async def consulta(termo: str):
    browser = app.state.browser
    consulta_id = gerar_id_consulta()

    async with sem:
        # semaforo controla o fluxo de consultas simultaneas
        resultados = await realizar_busca(browser, termo)

    if not resultados:
        message = (
            "Não foi possível retornar os dados no tempo solicitado."
            if termo.isdigit()
            else f"Foram encontrados 0 resultados para o termo: {termo}"
        )
        return {
            "consulta_id": consulta_id,
            "termo_busca": termo,
            "data_consulta": datetime.now(br_timezone).isoformat(),
            "message": message,
        }

    return {
        "consulta_id": consulta_id,
        "termo_busca": termo,
        "data_consulta": datetime.now(br_timezone).isoformat(),
        "resultados": resultados,
    }
