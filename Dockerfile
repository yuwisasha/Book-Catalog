FROM python:3.12

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - && \
    cd /usr/local/bin && \
    ln -s /etc/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

RUN bash -c "poetry install --no-root"

RUN bash -c "poetry add mysqlclient"

COPY . /app