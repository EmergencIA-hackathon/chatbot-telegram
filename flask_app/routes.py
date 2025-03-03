import os
import json
from flask import Blueprint, request, jsonify
from telegram import Update
from flask_app.controllers.bot_controller import processar_update, bot, get_loop
import asyncio
import nest_asyncio
from datetime import datetime

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
    if not nova_ocorrencia:
        return  # evita salvar ocorrências vazias

    ocorrencias = carregar_ocorrencias()
    ocorrencias.append(nova_ocorrencia)
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(ocorrencias, file, indent=4, ensure_ascii=False)

@api.route('/')
def index():
    return "Servidor Flask funcionando!"

@api.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Dados inválidos recebidos"}), 400

    asyncio.run_coroutine_threadsafe(processar_update(Update.de_json(data, bot=bot)), get_loop())
    return jsonify({"message": "Webhook recebido"}), 200

@api.route('/ocorrencias', methods=['GET'])
def listar_ocorrencias():
    return jsonify(carregar_ocorrencias())

@api.route('/ocorrencias', methods=['POST'])
def adicionar_ocorrencia():
    dados = request.json
    if all(k in dados for k in ["tipo", "conteudo", "chat_id", "usuario", "data_hora"]):
        salvar_ocorrencia(dados)
        return jsonify({"mensagem": "Ocorrência registrada com sucesso!"}), 201
    return jsonify({"erro": "Formato inválido. Certifique-se de enviar 'tipo', 'conteudo', 'chat_id', 'usuario' e 'data_hora'."}), 400
