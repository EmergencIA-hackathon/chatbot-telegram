FROM python:3.9-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y libmagic1

# Configuração do diretório de trabalho
WORKDIR /app

# Copiar os arquivos para dentro do contêiner
COPY . /app

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar a aplicação
CMD ["python", "bot.py"]
