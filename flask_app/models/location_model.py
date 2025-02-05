import aiohttp

async def obter_endereco_geocodexyz(latitude, longitude):
    url = f"https://geocode.xyz/{latitude},{longitude}?geoit=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            dados = await response.json()
            return dados.get('staddress', 'Endereço não disponível')
