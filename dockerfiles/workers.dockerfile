FROM python:3.9.7

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
WORKDIR /code/workers
COPY ./workers/pyproject.toml ./workers/poetry.lock* /code/workers/

RUN poetry install --no-root --no-dev

COPY ./workers /code/workers
WORKDIR /code

CMD ["rq", "worker"]
