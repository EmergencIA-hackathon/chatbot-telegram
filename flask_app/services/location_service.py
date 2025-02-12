from telegram import Update
from telegram.ext import CallbackContext
from models.location_model import coordenadas_para_endereco

async def receber_localizacao(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if update.message and update.message.location:
        latitude = update.message.location.latitude
        longitude = update.message.location.longitude
        endereco = coordenadas_para_endereco(latitude, longitude)

        if user_id in usuario_em_registro:
            usuario_em_registro[user_id]["localizacoes"].append({"latitude": latitude, "longitude": longitude, "endereco": endereco})
        else:
            usuario_em_registro[user_id] = {"ocorrencias": [], "fotos": [], "audios": [], "videos": [], "localizacoes": [{"latitude": latitude, "longitude": longitude, "endereco": endereco}]}

        await update.message.reply_text(f"📍 Localização registrada!\n{endereco}\nDeseja adicionar mais alguma coisa? (sim/não)")
