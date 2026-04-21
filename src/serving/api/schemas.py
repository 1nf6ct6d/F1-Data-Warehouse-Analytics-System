from pydantic import BaseModel


class DriverPointsResponse(BaseModel):
    driver_id: str
    given_name: str
    family_name: str
    nationality: str | None
    total_points: float


class ConstructorPointsResponse(BaseModel):
    constructor_id: str
    constructor_name: str
    nationality: str | None
    total_points: float


class DriverPodiumsResponse(BaseModel):
    driver_id: str
    given_name: str
    family_name: str
    podiums: int


class RaceResultsResponse(BaseModel):
    season: int
    round_number: int
    race_name: str
    race_date: str | None
    driver_id: str
    given_name: str
    family_name: str
    constructor_name: str
    grid_position: int | None
    finish_position: int | None
    position_text: str | None
    points: float | None
    status: str | None
    fastest_lap_time: str | None
    fastest_lap_avg_speed: float | None