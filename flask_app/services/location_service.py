from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from models.location_model import obter_endereco_geocodexyz

def pedir_localizacao(update, context):
    keyboard = [[KeyboardButton("📍 Compartilhar Localização", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Clique no botão abaixo para compartilhar sua localização:", reply_markup=reply_markup)

async def receber_localizacao(update: Update, context: CallbackContext):
    if update.message and update.message.location:
        latitude = update.message.location.latitude
        longitude = update.message.location.longitude
        endereco = obter_endereco_geocodexyz(latitude, longitude)
        await update.message.reply_text(f"📍 Localização recebida!\nLatitude: {latitude}\nLongitude: {longitude}\nEndereço: {endereco}")
    else:
        await update.message.reply_text("Não foi possível obter a sua localização.")
