FROM python:alpine as builder
LABEL maintainer="Filip Kania <hello@fkrq.me>"

RUN apk add build-base
RUN pip install --no-cache poetry

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --without dev --no-root --no-interaction

# --

FROM python:alpine as runtime

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv/
COPY src ./src/

ENV PATH "/app/.venv/bin:$PATH"

EXPOSE 8000

ENV PYTHONPATH .
CMD ["gunicorn", "src.app:async_app_factory", "--bind=0.0.0.0", "--worker-class=aiohttp.GunicornWebWorker"]
