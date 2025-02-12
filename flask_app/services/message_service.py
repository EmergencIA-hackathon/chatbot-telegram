from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
import re
import json
import requests

# mapeando o estado do usuário no registro de ocorrência
usuario_em_registro = {}

API_URL = "https://suaapi.com/ocorrencias"  

async def start(update: Update, context: CallbackContext) -> None:
    resposta = (
        "Olá! 👋 Sou o EmergêncIA, um bot de registro de ocorrências.\n"
        "Envie sua ocorrência diretamente ou clique abaixo para começar."
    )
    teclado = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="Registrar ocorrência", callback_data="enquete_ocorrencia"),
            InlineKeyboardButton(text="Saber mais sobre o serviço", callback_data="enquete_servico")
        ]
    ])
    await update.message.reply_text(resposta, reply_markup=teclado)

# lidar com mensagens de texto
async def responder(update: Update, context: CallbackContext) -> None:
    texto_mensagem = update.message.text.strip()
    user_id = update.message.from_user.id

    if user_id not in usuario_em_registro:
        # se o usuário já enviou uma ocorrência, registrar automaticamente
        if not re.search(r"\b(olá|oi|bom dia|boa tarde|boa noite|ei|hello|hey|salve)\b", texto_mensagem, re.IGNORECASE):
            usuario_em_registro[user_id] = {
                "ocorrencias": [],
                "fotos": [],
                "audios": [],
                "videos": [],
                "localizacoes": []
            }
            usuario_em_registro[user_id]["ocorrencias"].append(texto_mensagem)
            await update.message.reply_text(
                f"📝 Ocorrência registrada: '{texto_mensagem}'\n"
                "Deseja registrar mais alguma coisa? (sim/não)"
            )
            return

        await start(update, context)
        return

    estado_atual = usuario_em_registro[user_id]

    if texto_mensagem.lower() in ['sim', 's']:
        await update.message.reply_text("Pode enviar mais detalhes: texto, foto, áudio, vídeo ou localização.")
        return

    if texto_mensagem.lower() in ['não', 'nao', 'n', 'não quero mais registrar']:
        await finalizar_ocorrencia(update, user_id)
        return

    # se for uma nova ocorrência, armazenar
    estado_atual["ocorrencias"].append(texto_mensagem)
    await update.message.reply_text(
        f"📝 Ocorrência registrada: '{texto_mensagem}'\n"
        "Deseja registrar mais alguma coisa? (sim/não)"
    )

# finalizar e enviar a ocorrência para a API
async def finalizar_ocorrencia(update: Update, user_id: int):
    dados_ocorrencia = usuario_em_registro.pop(user_id, None)
    if not dados_ocorrencia:
        await update.message.reply_text("Erro ao processar a ocorrência. Tente novamente.")
        return

    # criar JSON para envio
    payload = json.dumps(dados_ocorrencia, ensure_ascii=False)
    response = requests.post(API_URL, data=payload, headers={"Content-Type": "application/json"})

    if response.status_code == 200:
        await update.message.reply_text("✅ Sua ocorrência foi enviada com sucesso para os agentes!")
    else:
        await update.message.reply_text(f"⚠️ Erro ao enviar a ocorrência. Código: {response.status_code}")

# callback para botões de enquete
async def callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "enquete_ocorrencia":
        usuario_em_registro[user_id] = {
            "ocorrencias": [],
            "fotos": [],
            "audios": [],
            "videos": [],
            "localizacoes": []
        }
        await query.message.reply_text(
            "📝 Envie agora sua ocorrência. Pode ser uma descrição por texto, foto, áudio, vídeo ou localização."
        )
    elif query.data == "enquete_servico":
        await query.message.reply_text(
            "Nós registramos qualquer tipo de ocorrência. Você pode enviar:\n"
            "📄 Texto explicando o ocorrido\n"
            "📸 Fotos\n"
            "🎤 Áudios\n"
            "📹 Vídeos\n"
            "📍 Localizações\n"
            "Nossa equipe analisará cada caso!"
        )
