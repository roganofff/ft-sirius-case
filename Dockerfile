

FROM ml_edition AS base

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       git \
       libgomp1 \
    && rm -rf /var/lib/apt/lists/*

FROM base AS deps

RUN pip install --no-cache-dir poetry

COPY requests_api/pyproject.toml requests_api/poetry.lock /app/requests_api/

# RUN cd /app/requests_api \
#     && poetry export -f requirements.txt --without-hashes > /app/requirements.txt

FROM base

WORKDIR /app

# COPY --from=deps /app/requirements.txt /app/requirements.txt

# RUN pip install --no-cache-dir \
#       -r requirements.txt \
#       fastapi uvicorn[standard] jinja2 openai requests
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
 && poetry install --only main --no-interaction --no-ansi

COPY chatbot    /app/chatbot
COPY requests_api /app/requests_api

EXPOSE 8000

CMD ["uvicorn", "chatbot.src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
