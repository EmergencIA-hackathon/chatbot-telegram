import os
import json
from flask import Blueprint, request, jsonify
from telegram import Update
from flask_app.controllers.bot_controller import processar_update, bot, get_loop
import asyncio
import nest_asyncio

nest_asyncio.apply()

api = Blueprint('api', __name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "ocorrencias.json")

def carregar_ocorrencias():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4, ensure_ascii=False)
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def salvar_ocorrencia(nova_ocorrencia):
    ocorrencias = carregar_ocorrencias()
    ocorrencias.append(nova_ocorrencia)
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(ocorrencias, file, indent=4, ensure_ascii=False)

@api.route('/')
def index():
    return "Servidor Flask funcionando!"

@api.route('/webhook', methods=['POST'])
def webhook():
    """Recebe atualizações do Telegram via webhook e as processa utilizando o loop global."""
    data = request.get_json()
    update = Update.de_json(data, bot=bot)
    salvar_ocorrencia({"tipo": "mensagem", "conteudo": str(data)})

    # Agenda a tarefa no loop global 
    asyncio.run_coroutine_threadsafe(processar_update(update), get_loop())
    
    return jsonify({"message": "Webhook recebido"}), 200

@api.route('/ocorrencias', methods=['GET'])
def listar_ocorrencias():
    return jsonify(carregar_ocorrencias())

@api.route('/ocorrencias', methods=['POST'])
def adicionar_ocorrencia():
    dados = request.json
    if "tipo" in dados and "conteudo" in dados:
        salvar_ocorrencia(dados)
        return jsonify({"mensagem": "Ocorrência registrada com sucesso!"}), 201
    return jsonify({"erro": "Formato inválido. Certifique-se de enviar 'tipo' e 'conteúdo'."}), 400
