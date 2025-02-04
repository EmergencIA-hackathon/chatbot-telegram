from flask import Flask, request, jsonify
from flask_app.controllers.bot_controller import main


app = Flask(__name__)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
