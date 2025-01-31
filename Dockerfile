FROM python:3.9-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y libmagic1 && rm -rf /var/lib/apt/lists/*

# Configuração do diretório de trabalho
WORKDIR /app

# Copiar os arquivos para dentro do contêiner
COPY . .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Definir comando de execução do bot
CMD ["python", "bot.py"]
