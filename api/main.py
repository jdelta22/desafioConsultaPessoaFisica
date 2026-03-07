import uuid
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

from scraper import realizar_busca

app = FastAPI()


class ConsultaRequest(BaseModel):
    termo: str


def gerar_id_consulta():
    uid = uuid.uuid4().hex[:8]
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    return f"{uid}_{timestamp}"


@app.get("/consulta/{termo_busca}")
async def api_buscar_detalhes_pessoa_fisica(termo_busca: str):

    consulta_id = gerar_id_consulta()
    resultados = await realizar_busca(termo_busca)

    if not resultados:
        if termo_busca.isdigit():
            return {
                "message": "Não foi possível retornar os dados no tempo de resposta solicitado."
            }
        else:
            return {"message": "Foram encontrados 0 resultados para o termo …"}

    return {
        "consulta_id": consulta_id,
        "termo_busca": termo_busca,
        "data_consulta": datetime.now().isoformat(),
        "resultados": resultados,
    }
