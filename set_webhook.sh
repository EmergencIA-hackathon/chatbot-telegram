#!/bin/bash

# Espera até o ngrok estar disponível
until curl -s http://ngrok:4040/api/tunnels | grep -q "public_url"; do
  echo "⏳ Aguardando o ngrok iniciar..."
  sleep 2
done

if [ -z "$TOKEN" ]; then
  echo "❌ Variável TELEGRAM_BOT_TOKEN não carregada corretamente."
  exit 1
fi


# Obtém o URL público do ngrok
NGROK_URL=$(curl -s http://ngrok:4040/api/tunnels | jq -r '.tunnels[0].public_url')

# Configura o webhook do Telegram
WEBHOOK_URL="$NGROK_URL/webhook"
TOKEN="${TELEGRAM_BOT_TOKEN}"

curl -s -X POST https://api.telegram.org/bot$TOKEN/setWebhook -d "url=$WEBHOOK_URL"

echo "Configurando webhook: https://api.telegram.org/bot$TOKEN/setWebhook com URL $WEBHOOK_URL"

