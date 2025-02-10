from flask import Flask, request, jsonify
from flask_app.controllers.bot_controller import main
from telegram import Update, Bot
from telegram.ext import Application
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

@app.route('/')
def index():
    return "Servidor Flask funcionando!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("Dados recebidos:", data)

        if 'message' not in data or 'date' not in data['message']:
            return jsonify({"error": "Formato inválido"}), 400

        update = Update.de_json(data, bot=bot)
        asyncio.run(application.initialize())
        asyncio.run(main(update, application))

        return 'Webhook recebido', 200

    except Exception as e:
        print("Erro:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
