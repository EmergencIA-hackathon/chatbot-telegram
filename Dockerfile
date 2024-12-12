# Usar uma imagem base do Python
FROM python:3.11-slim

# Definir o diretório de trabalho
WORKDIR /app

# Instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . .

# Expor a porta do servidor
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["python", "app/bot.py"]
