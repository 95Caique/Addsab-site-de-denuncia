# Dockerfile para Django
FROM python:3.10-slim

# Variáveis de ambiente para não gerar .pyc e buffer de logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas o requirements primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Criar diretórios para arquivos estáticos e de mídia
RUN mkdir -p /app/staticfiles /app/media

# Copiar o projeto
COPY . .

# Expor a porta 8000
EXPOSE 8000

# Comando padrão: desenvolvimento local
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]