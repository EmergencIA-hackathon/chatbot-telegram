# Imagem base para Python
FROM python:3.9

# Atualizar o sistema e instalar ffmpeg
USER root
RUN apt-get update && apt-get install -y ffmpeg

# Definir diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install -r /app/requirements.txt

# Copiar o código para o container
COPY . .

# Comando padrão
CMD ["python", "flask-app/app.py"]
