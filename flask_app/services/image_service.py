from PIL import Image
import pytesseract
from telegram import Update
from telegram.ext import CallbackContext
import asyncio
import re

async def handle_image(update: Update, context: CallbackContext):
    await processar_imagem_com_ocr(update, context)

async def processar_imagem_com_ocr(update: Update, context: CallbackContext):
    #Baixa a imagem corretamente usando await
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    await file.download_to_drive('imagem_recebida.jpg')

    #Abre a imagem com Pillow
    img = Image.open('imagem_recebida.jpg')

    #Usa pytesseract para fazer o OCR
    texto = pytesseract.image_to_string(img)

    #Usando regex para extrai apenas o cpf
    padrao_cpf = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
    match = re.search(padrao_cpf, texto)


    # Verifica se encontrou um CPF
    if match:
        cpf = match.group(0)
        resposta = f"CPF encontrado: {cpf}"
    else:
        resposta = "Nenhum CPF foi encontrado na imagem."

    await context.bot.send_message(chat_id=update.message.chat_id, text=resposta)