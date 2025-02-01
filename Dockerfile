# Imagem base para Python
FROM python:3.9

# Atualizar o sistema e instalar ffmpeg
USER root
RUN apt-get update && apt-get install -y ffmpeg

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código para o container
COPY . /app
WORKDIR /app

# Comando padrão
CMD ["python", "bot.py"]
