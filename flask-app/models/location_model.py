# flask-app/models/location_model.py
import requests

def obter_endereco_geocodexyz(latitude, longitude):
    url = f"https://geocode.xyz/{latitude},{longitude}?geoit=json"
    response = requests.get(url)
    dados = response.json()
    return dados.get('staddress', 'Endereço não disponível')
