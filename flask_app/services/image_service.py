from PIL import Image
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
    await file.download_to_drive(file_path)
    
    try:
        # Abre a imagem com Pillow
        img = Image.open(file_path)

        # Usa pytesseract para fazer o OCR
        texto = pytesseract.image_to_string(img)

        # Usando regex para extrair o CPF ou emplacamento de veículo
        padrao_cpf = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
        padrao_placa = r"[A-Z]{2,3}\d{1}[A-Z]{1,2}\d{2,3}"
        match_cpf = re.search(padrao_cpf, texto)
        match_placa = re.search(padrao_placa, texto)

        # verifica se encontrou um CPF
        if match_cpf:
            cpf = match_cpf.group(0)
            resposta = f"Imagem recebida com sucesso!\nCPF identificado: {cpf}"
        # verifica se encontrou o emplacamento de carro
        elif match_placa:
            placa = match_placa.group(0)
            resposta = f"Imagem recebida com sucesso!\nVeículo identificado, emplacamento: {placa}"
        else:
            resposta = "Imagem recebida com sucesso! Nenhuma informação relevante identificada."
    
    except Exception as e:
        resposta = f"Erro ao processar a imagem: {str(e)}"
    
    finally:
        # apagando o arquivo após o processamento
        if os.path.exists(file_path):
            os.remove(file_path)
    
    await context.bot.send_message(chat_id=update.message.chat_id, text=resposta)