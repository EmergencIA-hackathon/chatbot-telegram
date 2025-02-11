# Imagem base para Python
FROM python:3.9

# Atualizar o sistema e instalar ffmpeg
USER root
RUN apt-get update && apt-get install -y ffmpeg

# Definir diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install aiohttp
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código para o container
COPY . .

# Definir variável para garantir que Flask reconheça o diretório correto
ENV PYTHONPATH=/app

# Definir diretório correto para rodar o app
WORKDIR /app/flask_app

# Copiar o script para o container
COPY set_webhook.sh /app/set_webhook.sh

# Garantir que o script tenha permissão de execução
RUN chmod +x /app/set_webhook.sh

# Expor a porta para o app Flask
EXPOSE 5000

# Comando padrão para rodar o container
CMD /app/set_webhook.sh && gunicorn -w 1 -b 0.0.0.0:5000 app:app
