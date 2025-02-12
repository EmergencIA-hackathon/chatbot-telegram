import requests
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
from telegram import Update
from telegram.ext import CallbackContext

async def transcrever_audio(file_url: str) -> str:
    recognizer = sr.Recognizer()
    audio_response = requests.get(file_url)
    
    if audio_response.status_code == 200:
        audio_data = BytesIO(audio_response.content)
        try:
            audio = AudioSegment.from_file(audio_data)
            with NamedTemporaryFile(delete=True) as temp_wav_file:
                audio.export(temp_wav_file, format="wav")
                temp_wav_file.seek(0)
                with sr.AudioFile(temp_wav_file.name) as source:
                    audio = recognizer.record(source)
                    return recognizer.recognize_google(audio, language='pt-BR')
        except Exception as e:
            return f"Erro ao processar o áudio: {str(e)}"
    return "Erro ao baixar o áudio."

async def handle_audio(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    file_id = update.message.voice.file_id if update.message.voice else update.message.audio.file_id
    file = await context.bot.get_file(file_id)
    file_url = file.file_path

    transcricao = await transcrever_audio(file_url)

    if user_id in usuario_em_registro:
        usuario_em_registro[user_id]["audios"].append(transcricao)
    else:
        usuario_em_registro[user_id] = {"ocorrencias": [], "fotos": [], "audios": [transcricao], "videos": [], "localizacoes": []}

    await update.message.reply_text(
        f"📝 Áudio transcrito: '{transcricao}'\nDeseja registrar mais alguma coisa? (sim/não)"
    )
