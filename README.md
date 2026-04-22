# F1 Data Warehouse & Analytics System

Мой проект, в котором данные Формулы-1 проходят полный путь:

**API → raw layer → staging → DWH → serving → backend → demo frontend**
<img width="2532" height="1296" alt="image" src="https://github.com/user-attachments/assets/7a883563-c8cd-48fa-a37b-8d07d492f61e" />

---
## Технологический стек
**Язык и библиотеки:**
- Python
- requests
- pandas
- python-dotenv
- minio
- oracledb
- clickhouse-connect
- fastapi
- uvicorn

**Хранилища и сервисы:**
- MinIO
- Oracle Database
- ClickHouse

**Оркестрация:**
- Apache Airflow

**Инфраструктура:**
- Docker
- Docker Compose

**Интерфейс:**
- HTML
- CSS
- JavaScript

---
## О проекте

Проект реализует локальную аналитическую платформу для данных Формулы-1.

Источником данных выступает **Jolpica / Ergast F1 API**.  
Данные забираются, сохраняются в lake-слой, нормализуются, загружаются в хранилище, агрегируются и отдаются через API и demo UI.

Проект сделан как приближённая к production учебная система с разделением на слои:
- ingestion
- storage
- transform
- DWH
- serving
- orchestration
- API
- frontend

---

## Поддерживаемые сезоны

**В проект есть возможность загрузить следующие сезоны:

2021
2022
2023

*Архитектура позволяет расширить загрузку на большее количество сезонов. Дальнейшая гибкость системы будет развиваться в будущих обновлениях.*

## Примеры аналитики
- таблица очков пилотов
- таблица очков конструкторов
- подиумы пилотов
- результаты конкретной гонки по сезону и раунду

## Запуск

*Подробная инструкция для локального запуска находится в файле: ```docs/LOCAL_SETUP_RU.md```*


## Demo
**Backend**
- FastAPI docs: http://127.0.0.1:8000/docs

**Frontend**
- demo UI: http://127.0.0.1:5500/frontend/

**Airflow**
- UI: http://127.0.0.1:8088

## Что реализовано

### Data ingestion
- загрузка данных из F1 API
- загрузка сущностей:
  - races
  - drivers
  - constructors
  - results
- multi-season ingestion

### Storage layer
- raw JSON сохраняются локально и в MinIO
- staging CSV сохраняются локально и в MinIO

### Transform layer
- нормализация race data
- нормализация driver data
- нормализация constructor data
- нормализация race results

### DWH layer (Oracle)
- dimension tables:
  - `dim_race`
  - `dim_driver`
  - `dim_constructor`
- fact table:
  - `fact_race_result`

### Analytics layer
- Oracle views:
  - `vw_race_results`
  - `vw_driver_points`
  - `vw_constructor_points`
  - `vw_driver_podiums`

### Serving layer
- ClickHouse serving tables:
  - `srv_driver_points`
  - `srv_constructor_points`

### Backend
- FastAPI API
- endpoints:
  - `/health`
  - `/driver-points`
  - `/constructor-points`
  - `/driver-podiums`
  - `/race-results`

### Frontend
- demo UI на HTML/CSS/JS
- загрузка данных из FastAPI
- просмотр:
  - очков пилотов
  - очков конструкторов
  - подиумов
  - результатов гонок

### Orchestration
- Airflow DAG для multi-season pipeline
- orchestration основного пайплайна:
  - reset DWH
  - ingestion
  - normalize
  - dimension load
  - results load
  - fact load

---
<img width="1910" height="1131" alt="image" src="https://github.com/user-attachments/assets/b13b4773-e012-443b-af5a-74ff1cea7368" />


## Архитектура

```text
Jolpica F1 API
    ↓
Python ingestion
    ↓
Raw JSON (local + MinIO)
    ↓
Python transform / normalize
    ↓
Staging CSV (local + MinIO)
    ↓
Oracle DWH
(dimensions + fact + analytics views)
    ↓
ClickHouse serving layer
    ↓
FastAPI backend
    ↓
Demo frontend
```

## Структура проекта 

```text
airflow/
docs/
frontend/
infra/docker/
sql/oracle/
sql/clickhouse/
src/common/
src/ingestion/
src/transform/
src/dwh/
src/serving/
src/storage/
tests/
```
