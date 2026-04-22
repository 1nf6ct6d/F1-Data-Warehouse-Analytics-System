# Локальный запуск проекта F1 Data Warehouse & Analytics System

Этот документ нужен для пошагового запуска проекта с нуля.

---

## 1. Что нужно установить

Перед запуском у тебя должны быть установлены:

- Git
- Python 3.11+ или 3.12+
- Docker Desktop
- DBeaver
- VS Code

---

## 2. Клонирование проекта

```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd F1-Data-Warehouse-Analytics-System
```

## 3. Создание виртуального окружения
Windows 

```PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
## 4. Установка зависимостей
```pip install -r requirements.txt```

## 5. Создание .env

Скопируй `.env.example` в `.env`:

`copy .env.example .env`

Или создай вручную.

## 6. Поднятие инфраструктуры

Перейди в папку:

`cd infra/docker`

Подними сервисы:

`docker compose up -d minio oracle clickhouse`

Если нужен Airflow:

`docker compose up -d airflow-webserver airflow-scheduler`

## 7. Проверка сервисов
MinIO
`http://127.0.0.1:9001`

Oracle
`host: localhost`
`port: 1521`
`service name: FREEPDB1`

ClickHouse
`host: localhost`
`port: 8123`

Airflow
`http://127.0.0.1:8088`

## 8. Подключение к Oracle в DBeaver

Используй:
```text
Host: localhost
Port: 1521
Service Name: FREEPDB1
User: f1_dwh
Password: значение из .env
```

## 9. Первичная загрузка данных

Вернись в корень проекта.

Multi-season reload

Проект рассчитан на загрузку сезонов:

2021
2022
2023

Ты можешь прогонять пайплайн:

локальными Python-скриптами или через Airflow DAG

## 10. Инициализация ClickHouse
```
python -m src.serving.init_clickhouse
python -m src.serving.load_clickhouse_serving
```

## 11. Запуск backend
`uvicorn src.serving.api.app:app --reload`

Проверка:

`http://127.0.0.1:8000/docs`

## 12. Запуск frontend

Из корня проекта:

`python -m http.server 5500`

Проверка:

`http://127.0.0.1:5500/frontend/`
13. Запуск Airflow

Если сервисы уже подняты:

открой `http://127.0.0.1:8088`
логин: `admin`
пароль: `admin`

В Airflow доступен DAG для multi-season pipeline.

## 14. Что должно работать в итоге

После запуска должны быть доступны:
```
backend docs
demo frontend
airflow UI
minio console
Oracle DWH
ClickHouse serving layer
```