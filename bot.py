#!/usr/bin/python3
# coding: utf-8

import telepot, time, magic, os
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

# token do bot
TOKEN = "7729451424:AAH_AC4x2B1-ETZB5JA9JweOpJCXl4nqq9w"

DOWNLOADS_DIR = "/app/downloads"

# certificar-se de que a pasta de downloads existe
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

# função para lidar com mensagens
def principal(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type in ['document', 'audio', 'voice']:
        if content_type == 'document':
            file_id = msg['document']['file_id']
        elif content_type == 'audio':
            file_id = msg['audio']['file_id']
        elif content_type == 'voice':
            file_id = msg['voice']['file_id']

        # obtendo informações do arquivo e baixando
        file_info = bot.getFile(file_id)
        file_path = file_info['file_path']
        file_name = os.path.join(DOWNLOADS_DIR, file_path.split("/")[-1])

        bot.download_file(file_id, file_name)

        # identificando o tipo de arquivo
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_name)

        bot.sendMessage(chat_id, f"Arquivo baixado com sucesso! Tipo: {file_type}")

        # p/ arquivos de áudio
        if file_type.startswith("audio"):
            bot.sendMessage(chat_id, "Arquivo de áudio identificado! Transcrição em desenvolvimento.")

    elif content_type == 'text':
        texto_mensagem = msg.get('text', '').lower()
        print(f"Mensagem recebida de {chat_id}: {texto_mensagem}")

        # mensagem inicial
        if texto_mensagem in ['/start', 'olá', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'e aí', 'e ai', 'fala', 'hey', 'salve']:
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