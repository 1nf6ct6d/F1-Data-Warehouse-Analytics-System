from typing import Any

import requests


class F1ResultsApiClient:
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def get_results(self, season: int, round_number: int) -> Any:
        url = f"{self.endpoint}/{season}/{round_number}/results.json"

        try:
            response = requests.get(url, timeout=10)
        except requests.RequestException as exc:
            raise ConnectionError(f"Не удалось выполнить запрос к API: {url}") from exc

        response.raise_for_status()

        data = response.json()
        if not data:
            raise ValueError("API вернул пустой results-ответ")

        return data