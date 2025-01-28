#!/usr/bin/python3
# coding: utf-8

import telepot, time, magic
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

# Token do bot
TOKEN = "7729451424:AAH_AC4x2B1-ETZB5JA9JweOpJCXl4nqq9w"

# função para lidar com mensagens
def principal(msg):
    chat_id = msg['chat']['id']  # ID do chat
    texto_mensagem = msg.get('text', '').lower()  # convertendo a mensagem para minúscula

    print(f"Mensagem recebida de {chat_id}: {texto_mensagem}")

    # mensagens de início
    if texto_mensagem in ['/start', 'olá', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'e aí', 'fala', 'hey', 'salve']:
        resposta = "Olá! Gostaria de participar de uma enquete?"
        
        # botões de ação
        teclado = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Sim", callback_data="enquete_sim"),
             InlineKeyboardButton(text="Não", callback_data="enquete_nao")]
        ])
        bot.sendMessage(chat_id, resposta, reply_markup=teclado)
    
    # resposta para "tchau"
    elif texto_mensagem == "tchau":
        resposta = "Tchau! Tenha um ótimo dia!"
        bot.sendMessage(chat_id, resposta)

    # resposta padrão
    else:
        resposta = "Desculpe, não entendi sua mensagem. Tente novamente!"
        bot.sendMessage(chat_id, resposta)

# função para lidar com callbacks
def callback(query):
    query_id, from_id, dados = query['id'], query['from']['id'], query['data']

    print(f"Callback recebido de {from_id}: {dados}")

    # resposta de acordo com o botão clicado
    if dados == "enquete_sim":
        bot.sendMessage(from_id, "Obrigado por participar! Sua resposta foi: Sim.")
    elif dados == "enquete_nao":
        bot.sendMessage(from_id, "Tudo bem! Sua resposta foi: Não.")
    else:
        bot.sendMessage(from_id, "Opção inválida.")

    # notificar o clique
    bot.answerCallbackQuery(query_id)

        

# inicializando o bot
bot = telepot.Bot(TOKEN)

# configurando o bot para ouvir mensagens e interações
MessageLoop(bot, {'chat': principal, 'callback_query': callback}).run_as_thread()
print("Bot está funcionando...")

# manter em execução
while True:
    time.sleep(10)
