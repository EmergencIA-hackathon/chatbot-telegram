#!/bin/bash

# Obtém o URL público do ngrok
NGROK_URL=$(curl -s http://ngrok:4040/api/tunnels | jq -r '.tunnels[0].public_url')

# Configura o webhook do Telegram
WEBHOOK_URL="$NGROK_URL/webhook"
TOKEN="$TELEGRAM_BOT_TOKEN"

curl -s -X POST https://api.telegram.org/bot$TOKEN/setWebhook -d "url=$WEBHOOK_URL"

echo "✅ Webhook configurado em: $WEBHOOK_URL"
