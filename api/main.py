from fastapi import FastAPI

from scraper import realizar_busca

app = FastAPI()


@app.get("/buscarbeneficios/{termo_busca}")
async def api_buscar_detalhes_pessoa_fisica(termo_busca: str):

    resultados = await realizar_busca(termo_busca)

    if not resultados:
        if termo_busca.isdigit():
            return {
                "message": "Não foi possível retornar os dados no tempo de resposta solicitado."
            }
        else:
            return {"message": "Foram encontrados 0 resultados para o termo …"}

    return {"Termo de busca": termo_busca, **resultados}
