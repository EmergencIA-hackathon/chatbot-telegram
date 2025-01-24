#!/usr/bin/python3
#coding: utf-8 

import telepot, time
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton #bibliotecas p/ os botões

TOKEN = "7729451424:AAH_AC4x2B1-ETZB5JA9JweOpJCXl4nqq9w"

def handle_message(msg):
    chat_id = msg['chat']['id']  # ID do chat
    message_text = msg.get('text', '').lower()  # convertendo toda msg para minúscula

    print(f"Mensagem recebida de {chat_id}: {message_text}")

    # verificação
    if message_text in ["olá", "oi", "ei", "bom dia", "boa tarde", "boa noite"]:
        response = "Olá! Gostaria de participar de uma enquete?"
        # botões de ação
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Sim", callback_data="enquete_sim"),
             InlineKeyboardButton(text="Não", callback_data="enquete_nao")]
        ])
        bot.sendMessage(chat_id, response, reply_markup=keyboard)
    elif message_text == "tchau":
        response = "Tchau! Tenha um ótimo dia!"
        bot.sendMessage(chat_id, response)
    else:
        response = "Desculpe, não entendi sua mensagem. Tente novamente!"
        bot.sendMessage(chat_id, response)

def handle_callback(query):
    query_id, from_id, data = query['id'], query['from']['id'], query['data']

    print(f"Callback recebido de {from_id}: {data}")

    # resposta de acordo c/ botão clicado
    if data == "enquete_sim":
        bot.sendMessage(from_id, "Obrigado por participar! Sua resposta foi: Sim.")
    elif data == "enquete_nao":
        bot.sendMessage(from_id, "Tudo bem! Sua resposta foi: Não.")
    else:
        bot.sendMessage(from_id, "Opção inválida.")

    # notificar clique
    bot.answerCallbackQuery(query_id)

# inicializando
bot = telepot.Bot(TOKEN)

# configuração p/ o bot para ouvir mensagens e interações
MessageLoop(bot, {'chat': handle_message, 'callback_query': handle_callback}).run_as_thread()
print("Bot está funcionando...")

# manter rodando
import time
while True:
    time.sleep(10)




