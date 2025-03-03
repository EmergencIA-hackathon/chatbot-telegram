from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import pytesseract
from telegram import Update
from telegram.ext import CallbackContext
import asyncio
import re
import os

async def handle_image(update: Update, context: CallbackContext):
    await processar_imagem_com_ocr(update, context)

async def processar_imagem_com_ocr(update: Update, context: CallbackContext):
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    file_path = "imagem_recebida.jpg"
    # Aguarda o download do arquivo para o disco
    await file.download_to_drive(file_path)
    
    try:
        # Abre a imagem em uma thread separada
        img = await asyncio.to_thread(Image.open, file_path)
        texto = await asyncio.to_thread(pytesseract.image_to_string, img)
        

        # Regex para identificar CPF e placa:
        padrao_cpf = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
        match_cpf = re.search(padrao_cpf, texto)
        if match_cpf:
            cpf = match_cpf.group(0)
            resposta = f"Imagem recebida com sucesso!\nCPF identificado: {cpf}"
        else:
            # Envia o texto extraído para ajudar no debug
            resposta = "Imagem recebida com sucesso!"
    
    except Exception as e:
        resposta = f"Erro ao processar a imagem: {str(e)}"
    
    finally:
        if os.path.exists(file_path):
            await asyncio.to_thread(os.remove, file_path)
    
    await context.bot.send_message(chat_id=update.message.chat_id, text=resposta)
