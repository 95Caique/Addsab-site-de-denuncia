FROM python:3.9-alpine3.13

# Copia os arquivos necessários
COPY ./requirements.txt /tmp/requirements.txt
COPY . /app

# Define o diretório de trabalho
WORKDIR /app

# Expõe a porta padrão do Django
EXPOSE 8000

# Instala dependências e cria ambiente virtual
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Define o PATH e o usuário não-root
ENV PATH="/py/bin:$PATH"
USER django-user
