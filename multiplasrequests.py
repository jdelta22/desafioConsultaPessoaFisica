import asyncio

import httpx

base_url = "https://hook.us2.make.com/2gyaghd6i4e072tridxuvlrr8caounuk"

termos = ["12345678900", "98765432100", "gilberto nunes", "maria silva", "11122233344"]
termos1 = ["MARIO MARIO LEAL INCIARTE"]


async def enviar(termo):
    async with httpx.AsyncClient() as client:
        r = await client.get(base_url, params={"termo": termo})
        print(termo, r.status_code)


async def main():
    await asyncio.gather(*[enviar(t) for t in termos1])


asyncio.run(main())
