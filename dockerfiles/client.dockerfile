FROM python:3.9.7

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
WORKDIR /code/app
COPY ./app/pyproject.toml ./app/poetry.lock* /code/app/

RUN poetry install --no-root --no-dev

COPY ./app /code/app
WORKDIR /code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
