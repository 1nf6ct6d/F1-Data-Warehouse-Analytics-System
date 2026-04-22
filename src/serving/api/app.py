from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from src.serving.api.clickhouse_queries import (
    fetch_constructor_points_from_clickhouse,
    fetch_driver_points_from_clickhouse,
)
from src.serving.api.queries import (
    fetch_available_seasons,
    fetch_driver_podiums,
    fetch_race_results,
)
from src.serving.api.schemas import (
    ConstructorPointsResponse,
    DriverPodiumsResponse,
    DriverPointsResponse,
    RaceResultsResponse,
)

app = FastAPI(title="F1 DWH Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


@app.get("/available-seasons", response_model=list[int])
def get_available_seasons():
    return fetch_available_seasons()


@app.get("/driver-points", response_model=list[DriverPointsResponse])
def get_driver_points(limit: int = Query(default=20, ge=1, le=100)):
    return fetch_driver_points_from_clickhouse(limit=limit)


@app.get("/constructor-points", response_model=list[ConstructorPointsResponse])
def get_constructor_points(limit: int = Query(default=20, ge=1, le=100)):
    return fetch_constructor_points_from_clickhouse(limit=limit)


@app.get("/driver-podiums", response_model=list[DriverPodiumsResponse])
def get_driver_podiums(limit: int = Query(default=20, ge=1, le=100)):
    return fetch_driver_podiums(limit=limit)


@app.get("/race-results", response_model=list[RaceResultsResponse])
def get_race_results(
    season: int = Query(..., ge=2000, le=2100),
    round_number: int = Query(..., ge=1, le=30),
):
    return fetch_race_results(season=season, round_number=round_number)