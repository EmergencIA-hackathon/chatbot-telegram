import requests
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
from telegram import Update
from telegram.ext import CallbackContext
import asyncio

async def transcrever_audio(file_url: str) -> str:
    recognizer = sr.Recognizer()
    
    async def baixar_audio():
        return requests.get(file_url)
    
    audio_response = await asyncio.to_thread(baixar_audio)
    
    if audio_response.status_code == 200:
        audio_data = BytesIO(audio_response.content)
        try:
            audio = await asyncio.to_thread(AudioSegment.from_file, audio_data)
            with NamedTemporaryFile(delete=True) as temp_wav_file:
                await asyncio.to_thread(audio.export, temp_wav_file, format="wav")
                temp_wav_file.seek(0)
                with sr.AudioFile(temp_wav_file.name) as source:
                    audio = recognizer.record(source)
                    return await asyncio.to_thread(recognizer.recognize_google, audio, language='pt-BR')
        except Exception as e:
            return f"Erro ao processar o áudio: {str(e)}"
    return "Erro ao baixar o áudio."

async def handle_audio(update: Update, context: CallbackContext) -> None:
    file_id = update.message.voice.file_id if update.message.voice else update.message.audio.file_id
    file = await context.bot.get_file(file_id)
    file_url = file.file_path
    transcricao = await transcrever_audio(file_url)
    await update.message.reply_text(
        f"📝 Ocorrência registrada com sucesso: '{transcricao}'\nDeseja registrar mais alguma coisa? (sim/não)"
    )
    context.user_data["registrando_ocorrencia"] = True
