from telegram import Update
from telegram.ext import CallbackContext
from models.location_model import coordenadas_para_endereco  
import asyncio

async def receber_localizacao(update: Update, context: CallbackContext):
    if update.message and update.message.location:
        latitude = update.message.location.latitude
        longitude = update.message.location.longitude
        # Aguarda a execução da função assíncrona coordenadas_para_endereco
        endereco = await coordenadas_para_endereco(latitude, longitude)
        
        await update.message.reply_text(
            f"📍 Localização recebida!\nLatitude: {latitude}\nLongitude: {longitude}\nEndereço: {endereco}\n\n\nDeseja registrar mais alguma coisa? (sim/não)"
        )
    else:
        print("Não foi possível obter a sua localização.")
