#!/usr/bin/python3
# coding: utf-8

import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton 
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext, Application
import requests
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
from local import obter_endereco_geocodexyz
# Token do bot
TOKEN = "7729451424:AAH_AC4x2B1-ETZB5JA9JweOpJCXl4nqq9w"

# Função para lidar com o comando /start
async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    resposta = "Olá! Gostaria de participar de uma enquete?"
    
    # Criando botões
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Sim", callback_data="enquete_sim"),
         InlineKeyboardButton(text="Não", callback_data="enquete_nao")]
    ])
    
    await update.message.reply_text(resposta, reply_markup=teclado)

# Função para lidar com mensagens comuns
async def responder(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    texto_mensagem = update.message.text.lower()

    print(f"Mensagem recebida de {chat_id}: {texto_mensagem}")

    if texto_mensagem in ['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'e aí', 'fala', 'hey', 'salve']:
        await start(update, context)
    elif texto_mensagem == "tchau":
        await update.message.reply_text("Tchau! Tenha um ótimo dia!")
    else:
        await update.message.reply_text("Desculpe, não entendi sua mensagem. Tente novamente!")

# Função para lidar com callbacks 
async def callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Responde ao clique no botão

    print(f"Callback recebido de {query.from_user.id}: {query.data}")

    if query.data == "enquete_sim":
        await query.message.reply_text("Obrigado por participar! Sua resposta foi: Sim.")
    elif query.data == "enquete_nao":
        await query.message.reply_text("Tudo bem! Sua resposta foi: Não.")
    else:
        await query.message.reply_text("Opção inválida.")

# Função para transcrever áudio
async def transcrever_audio(file_url: str) -> str:
    recognizer = sr.Recognizer()

    # Fazendo download do arquivo diretamente da URL (API Telegram)
    audio_response = requests.get(file_url)
    if audio_response.status_code == 200:
        audio_data = BytesIO(audio_response.content)

        try:
            # Converter para WAV usando pydub (caso não esteja no formato correto)
            audio = AudioSegment.from_file(audio_data)
            with NamedTemporaryFile(delete=True) as temp_wav_file:
                audio.export(temp_wav_file, format="wav")
                temp_wav_file.seek(0)
                
                # Usar o speech_recognition para reconhecer o áudio
                with sr.AudioFile(temp_wav_file.name) as source:
                    audio = recognizer.record(source)
                    texto = recognizer.recognize_google(audio, language='pt-BR')
                    return texto
        except Exception as e:
            return f"Erro ao processar o áudio: {str(e)}"
    return "Erro ao baixar o áudio."

# Função para lidar com áudio e mensagens de voz
async def handle_audio(update: Update, context: CallbackContext) -> None:
    # Verifica se é áudio ou voice
    file_id = update.message.voice.file_id if update.message.voice else update.message.audio.file_id

    # Pega a URL do arquivo usando o Telegram API
    file = await context.bot.get_file(file_id)
    file_url = file.file_path

    # Transcreve o áudio
    transcricao = await transcrever_audio(file_url)

    # Envia a transcrição de volta ao usuário
    await update.message.reply_text(f"Transcrição: {transcricao}")



# FUNÇÃO PARA PEDIR A LOCALIZAÇÃO
def pedir_localizacao(update, context):
    keyboard = [[KeyboardButton("📍 Compartilhar Localização", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Clique no botão abaixo para compartilhar sua localização em tempo real:", reply_markup=reply_markup)

async def receber_localizacao(update, context):
    if update.message and update.message.location:  # Verifica se a mensagem e a localização estão presentes
        latitude = update.message.location.latitude
        longitude = update.message.location.longitude
        endereco = obter_endereco_geocodexyz(latitude, longitude)
        await update.message.reply_text(f"📍 Localização recebida!\nLatitude: {latitude}\nLongitude: {longitude}\nENDEREÇO: {endereco}")
      
       

    elif update.message:  # Verifica se a mensagem está presente antes de tentar responder
        await update.message.reply_text("Não foi possível obter a sua localização.")


# Função principal para rodar o bot
def main():
    app = Application.builder().token(TOKEN).build()

    # Adicionando handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.add_handler(CallbackQueryHandler(callback))
    # Handlers para mensagens de áudio e voz
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
    #handlers para a localização
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("📍 Compartilhar Localização"), pedir_localizacao))
    app.add_handler(MessageHandler(filters.LOCATION, receber_localizacao)) 


    print("Bot está rodando...")
    app.run_polling()

# Iniciar o bot
if __name__ == "__main__":
    main()
