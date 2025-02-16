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




    #Usando regex para extrair o cpf ou emplacamento veiculo
    padrao_cpf = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
    padrao_placa = r"[A-Z]{2,3}\d{1}[A-Z]{1,2}\d{2,3}"
    match_cpf = re.search(padrao_cpf, texto)
    match_placa= re.search(padrao_placa, texto)

    #Verifica se encontrou um CPF
    if match_cpf:
        cpf = match_cpf.group(0)
        resposta = f"Imagem recebida com sucesso!\nCPF identificado: {cpf}"
    #Verifica se encontrou emplacamento de carro
    elif match_placa:
        placa = match_placa.group(0)
        resposta = f"Imagem recebida com sucesso!\nVeiculo identificado, emplacamento: {placa}"
    else:
        resposta = "Imagem recebida com sucesso!."

    await context.bot.send_message(chat_id=update.message.chat_id, text=resposta)