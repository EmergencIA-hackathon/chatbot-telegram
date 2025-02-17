from flask import Blueprint, request, jsonify
from flask_app.controllers.bot_controller import main
from telegram import Update, Bot
from telegram.ext import Application
import os
import json
import asyncio

api = Blueprint('api', __name__)

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "ocorrencias.json")

def carregar_ocorrencias():
    """Carrega as ocorrências do arquivo JSON ou cria um novo se não existir."""
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4, ensure_ascii=False)
    
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def salvar_ocorrencia(nova_ocorrencia):
    """Adiciona uma nova ocorrência ao JSON"""
    ocorrencias = carregar_ocorrencias()
    ocorrencias.append(nova_ocorrencia)
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(ocorrencias, file, indent=4, ensure_ascii=False)

async def init_application():
    global application
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

loop = asyncio.get_event_loop()
loop.run_until_complete(init_application())

@api.route('/')
def index():
    return "Servidor Flask funcionando!"

@api.route('/webhook', methods=['POST'])
async def webhook():
    """Recebe mensagens do Telegram e salva no JSON"""
    data = request.get_json()
    update = Update.de_json(data, bot=bot)

    salvar_ocorrencia({"tipo": "mensagem", "conteudo": str(data)})

    await main(update, application)
    return jsonify({"message": "Webhook recebido"}), 200

@api.route('/ocorrencias', methods=['GET'])
def listar_ocorrencias():
    return jsonify(carregar_ocorrencias())

@api.route('/ocorrencias', methods=['POST'])
def adicionar_ocorrencia():
    """Adiciona uma nova ocorrência manualmente"""
    dados = request.json
    if "tipo" in dados and "conteudo" in dados:
        salvar_ocorrencia(dados)
        return jsonify({"mensagem": "Ocorrência registrada com sucesso!"}), 201
    return jsonify({"erro": "Formato inválido. Certifique-se de enviar 'tipo' e 'conteudo'."}), 400
