from flask import Flask, request, jsonify
from flask_app.controllers.bot_controller import main
from telegram import Update
from telegram import Bot
from telegram.ext import Application
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do .env

app = Flask(__name__)

@app.route('/')
def index():
    return "Servidor Flask funcionando!" 

@app.route('/webhook', methods=['POST'])
async def webhook():
    data = request.get_json()

    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    update = Update.de_json(data, bot=bot)

    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    await application.initialize()  
    await main(update, application)

    return 'Webhook recebido', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
