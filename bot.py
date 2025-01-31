#!/usr/bin/python3
# coding: utf-8

import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext

# Token do bot
TOKEN = "7729451424:AAH_AC4x2B1-ETZB5JA9JweOpJCXl4nqq9w"

# Função para lidar com o comando /start
async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    resposta = "Olá! Gostaria de participar de uma enquete?"
    
    # Criando botões inline
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

# Função para lidar com callbacks de botões
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

# Função principal para rodar o bot
def main():
    app = Application.builder().token(TOKEN).build()

    # Adicionando handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.add_handler(CallbackQueryHandler(callback))

    print("Bot está rodando...")
    app.run_polling()

# Iniciar o bot
if __name__ == "__main__":
    main()

