# Imagem base para Python
FROM python:3.9

# Atualizar o sistema e instalar ffmpeg
USER root
RUN apt-get update && apt-get install -y ffmpeg

# Definir diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install aiohttp


# Copiar o código para o container
COPY . .

# Definir variável para garantir que Flask reconheça o diretório correto
ENV PYTHONPATH=/app

# Definir diretório correto para rodar o app
WORKDIR /app/flask_app

# Comando padrão para rodar o container
CMD ["python", "app.py"]
