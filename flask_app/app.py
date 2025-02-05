from flask import Flask, request, jsonify
from flask_app.controllers.bot_controller import main
from telegram import Update
from telegram.ext import CallbackContext
from telegram import Bot
import asyncio

app = Flask(__name__)

@app.route('/')
def index():
    return "Servidor Flask funcionando!" 

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Criar objeto Update do Telegram com os dados recebidos
    update = Update.de_json(data, bot=Bot(token="7729451424:AAH_AC4x2B1-ETZB5JA9JweOpJCXl4nqq9w"))

    asyncio.run(main(update))

    return 'Webhook recebido', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
