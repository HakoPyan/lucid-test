FROM python:3.11-slim as base

FROM base as app_builder
COPY ./poetry.lock /src/poetry.lock
COPY ./pyproject.toml /src/pyproject.toml

WORKDIR /src
RUN pip install --no-cache-dir -U pip==23.0.1 poetry==1.4.0 \
    && python -m venv /env \
    && . /env/bin/activate \
    && poetry install --only main

FROM base as app
ARG VERSION=0.0.0
ENV VERSION=$VERSION
COPY --from=app_builder /env /env
COPY . /src
ENV PYTHONPATH=/src
ENV PATH="/env/bin:${PATH}"
WORKDIR /src
CMD ["uvicorn", "app.asgi:app", "--host", "0.0.0.0"]
