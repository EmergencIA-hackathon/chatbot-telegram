import aiohttp
import asyncio
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
from telegram import Update
from telegram.ext import CallbackContext

async def transcrever_audio(file_url: str) -> str:
    recognizer = sr.Recognizer()
    
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            if response.status == 200:
                audio_data = BytesIO(await response.read())  # Aguarda o download de forma assíncrona
                try:
                    audio = AudioSegment.from_file(audio_data)
                    with NamedTemporaryFile(delete=True, suffix=".wav") as temp_wav_file:
                        audio.export(temp_wav_file.name, format="wav")
                        with sr.AudioFile(temp_wav_file.name) as source:
                            audio = recognizer.record(source)
                            return recognizer.recognize_google(audio, language='pt-BR')
                except Exception as e:
                    return f"Erro ao processar o áudio: {str(e)}"
    return "Erro ao baixar o áudio."

async def handle_audio(update: Update, context: CallbackContext) -> None:
    file_id = update.message.voice.file_id if update.message.voice else update.message.audio.file_id
    file = await context.bot.get_file(file_id)
    file_url = file.file_path

    transcricao = await transcrever_audio(file_url)  # Aguarda a transcrição do áudio

    await update.message.reply_text(
        f"📝 Ocorrência registrada com sucesso: '{transcricao}'\nDeseja registrar mais alguma coisa? (sim/não)"
    )

    context.user_data["registrando_ocorrencia"] = True
