#!/usr/bin/python3 
#coding: utf-8 
import telepot, time

def principal(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
#content_type: tipo de conteúdo // define como tratar oq está sendo recebido
    if content_type == 'text':
        chat_id = msg['chat']['id']
        mensagem = msg['text']

        if mensagem.upper() == 'OI':
            send_message(chat_id, "Olá, mundo!")


telepot.Bot('7707515489:AAFbGoP6OJGfK2yeVbtDZK5CXb1cV9szz4c')

bot.message_loop(principal)

while 1:
    time.sleep(5)