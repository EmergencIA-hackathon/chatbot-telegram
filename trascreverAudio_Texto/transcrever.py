#para fazer a instalaçao da biblioteca é preciso ter o git
#É nessessario fazer o download do ffmpeg
import whisper

def  transcrever(audio):
    modelo = whisper.load_model("base")
    audio_path = audio #aqui esta recebendo o audio
    audio_transcrito = modelo.transcribe(audio_path) #trasncreve o audio para texto
    
    return audio_transcrito["text"]



