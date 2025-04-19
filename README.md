
# ft-sirius-case

Проект для обработки пользовательских запросов с использованием FastAPI, с поддержкой нескольких маршрутов, логики сравнения, чата и запросов.

## 📦 Стек технологий

- Python 3.11
- FastAPI
- Docker / Docker Compose
- Poetry
- Prometheus
- Grafana
- HTML + Jinja2
- PostgreSQL
- ClickHouse

---

## 🚀 Быстрый старт

1. Клонируй репозиторий:
```bash
git clone https://github.com/yourname/ft-sirius-case.git
cd ft-sirius-case
```

2. Собери и запусти контейнеры:
```bash
docker-compose up --build
```

3. Приложение будет доступно на:
- FastAPI API: [http://localhost:8000](http://localhost:8000)
- Метрики Prometheus: [http://localhost:8000/metrics](http://localhost:8000/metrics)
- Интерфейс Prometheus: [http://localhost:9090](http://localhost:9090)

---

## 📈 Метрики

Проект использует [`prometheus-fastapi-instrumentator`](https://github.com/trallnag/prometheus-fastapi-instrumentator), чтобы отслеживать производительность и логи запросов FastAPI.

Метрики доступны по адресу `/metrics`.

---

## 🧠 Структура проекта

```
.
├── chatbot
│   └── src
│       ├── api
│       │   └── routes
│       ├── models
│       ├── static
│       └── templates
├── requests_api        
│   └── src
│       └── app
│           ├── config.py
│           ├── db
│           ├── models
│           ├── routes
│           ├── utils
│           └── main.py
├── prometheus.yml
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## 📬 Основные эндпоинты

| Метод | URL              | Описание                 |
|-------|------------------|--------------------------|
| GET   | `/metrics`       | Метрики Prometheus       |
| POST  | `/chat/ask`      | Обработка запроса чата   |
| POST  | `/prompt/query`  | Работа с промптами       |
| POST  | `/requests`      | API по работе с вопросами|

---

## 🛠️ Поддержка и разработка

Если вы хотите доработать функциональность — используйте Poetry:
```bash
poetry install
poetry run uvicorn chatbot.src.api.main:app --reload
```

---

## 🧑‍💻 Team NoKeepish

- Демьяненко Вячеслав
- Колкарёва Даяна
- Прокаев Сергей
- Малкова Кристина
- Роганов Егор

---

## 📄 Лицензия

MIT License
