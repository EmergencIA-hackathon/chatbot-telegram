from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
import re

# mapeando se o usuário já respondeu a enquete
usuario_em_registro = {}

async def start(update: Update, context: CallbackContext) -> None:
    resposta = (
        "Olá! 👋 Sou o EmergêncIA, um bot de registro de ocorrências.\n"
        "Posso te ajudar a registrar algo?"
    )
    teclado = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="Sim, registrar ocorrência", callback_data="enquete_ocorrencia"),
            InlineKeyboardButton(text="Quero saber mais sobre o serviço", callback_data="enquete_servico")
        ]
    ])
    await update.message.reply_text(resposta, reply_markup=teclado)

# lidar com texto
async def responder(update: Update, context: CallbackContext) -> None:
    texto_mensagem = update.message.text.strip().lower()
    user_id = update.message.from_user.id

    print(f"Mensagem recebida: {texto_mensagem}")  # Debug

    if user_id in usuario_em_registro:
        if usuario_em_registro[user_id] == 'registrando_ocorrencia':
            if texto_mensagem:
                await update.message.reply_text(
                    f"📝 Ocorrência registrada: {texto_mensagem}\n"
                    "Deseja registrar mais alguma coisa? (sim/não)"
                )
                usuario_em_registro[user_id] = 'esperando_confirmacao'
                return

        elif usuario_em_registro[user_id] == 'esperando_confirmacao':
            if texto_mensagem in ['sim', 's']:
                await update.message.reply_text("Por favor, envie sua próxima ocorrência.")
                usuario_em_registro[user_id] = 'registrando_ocorrencia'
            elif texto_mensagem in ['não', 'nao', 'não quero mais registrar']:
                await update.message.reply_text("Obrigado por registrar sua ocorrência. Fique à vontade para voltar quando precisar.")
                del usuario_em_registro[user_id]
            else:
                await update.message.reply_text("Desculpe, não entendi sua resposta. Deseja registrar mais alguma coisa? (sim/não)")

    else:
        padrao_saudacao = r"\b(olá|oi{1,3}|bom dia|boa tarde|boa noite|ei|hello|hey|salve)\b"
        if re.search(padrao_saudacao, texto_mensagem):
            await start(update, context)
        elif texto_mensagem == "tchau":
            await update.message.reply_text("Tchau! Tenha um ótimo dia!")
        else:
            await update.message.reply_text(
                "Desculpe, não entendi sua mensagem. Se for uma ocorrência, "
                "envie texto, foto, áudio ou localização para registro."
            )

# callback para botões da enquete
async def callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "enquete_ocorrencia":
        usuario_em_registro[user_id] = 'registrando_ocorrencia'
        await query.message.reply_text(
            "📝 Perfeito! Envie agora sua ocorrência. Pode ser uma descrição por texto, foto, áudio ou localização."
        )
    elif query.data == "enquete_servico":
        await query.message.reply_text(
            "Nós registramos qualquer tipo de ocorrência, independente da situação. Conte com a gente para registrar e encaminhar seu relato! Você pode enviar:\n"
            "📄 Texto explicando o ocorrido\n"
            "📸 Fotos\n"
            "🎤 Áudios\n"
            "📍 Localizações\n"
            "Nosso time de agentes analisará cada caso e entrará em contato se necessário."
        )
