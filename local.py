import requests

def obter_endereco_geocodexyz(latitude, longitude):
    url = f"https://geocode.xyz/{latitude},{longitude}?geoit=json"
    
    response = requests.get(url)
    dados = response.json()
    
    if 'staddress' in dados:
        endereco = dados.get('staddress', 'Endereço não disponível')
        return endereco
    else:
        return "Endereço não encontrado"
    


