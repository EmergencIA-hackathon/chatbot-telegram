# Imagem base para Python
FROM python:3.9

# Atualizar o sistema e instalar ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Copiar o código da aplicação para o container
COPY . .

# Definir variável para garantir que Flask reconheça o diretório correto
ENV PYTHONPATH=/app

# Expor a porta do Flask
EXPOSE 5000

# Comando padrão para rodar o container
CMD ["gunicorn", "-w", "1", "-k", "gthread", "-b", "0.0.0.0:5000", "flask_app.app:app"]
