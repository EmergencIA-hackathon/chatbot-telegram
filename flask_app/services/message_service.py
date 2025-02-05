from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

async def start(update: Update, context: CallbackContext) -> None:
    resposta = "Olá! Gostaria de participar de uma enquete?"
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Sim", callback_data="enquete_sim"),
         InlineKeyboardButton(text="Não", callback_data="enquete_nao")]
    ])
    await update.message.reply_text(resposta, reply_markup=teclado)

async def responder(update: Update, context: CallbackContext) -> None:
    texto_mensagem = update.message.text.lower()
    print(f"Mensagem recebida: {texto_mensagem}")  # Debug
    if texto_mensagem in ['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite']:
        await start(update, context)
    elif texto_mensagem == "tchau":
        await update.message.reply_text("Tchau! Tenha um ótimo dia!")
    else:
        await update.message.reply_text("Desculpe, não entendi sua mensagem. Tente novamente!")

async def callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "enquete_sim":
        await query.message.reply_text("Obrigado por participar! Sua resposta foi: Sim.")
    elif query.data == "enquete_nao":
        await query.message.reply_text("Tudo bem! Sua resposta foi: Não.")
