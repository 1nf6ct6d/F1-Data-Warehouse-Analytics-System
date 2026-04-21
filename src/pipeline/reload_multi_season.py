from src.ingestion.load_entity import load_single_entity
from src.ingestion.load_results_season import load_results_for_season
from src.transform.normalize_races import main as normalize_races_main
from src.transform.normalize_drivers import main as normalize_drivers_main
from src.transform.normalize_constructors import main as normalize_constructors_main
from src.transform.normalize_results_season import normalize_results_for_season
from src.dwh.reset_dwh import main as reset_dwh_main
from src.dwh.load_dimensions import main as load_dimensions_main
from src.dwh.load_fact_race_result_season import load_fact_for_season


SEASONS = [2021, 2022, 2023]


def main() -> None:
    print("[PIPELINE] Старт multi-season reload")

    reset_dwh_main()

    for season in SEASONS:
        print(f"[PIPELINE] === season={season} ===")

        load_single_entity(season=season, entity="races")
        load_single_entity(season=season, entity="drivers")
        load_single_entity(season=season, entity="constructors")

        normalize_races_main()
        normalize_drivers_main()
        normalize_constructors_main()

        load_dimensions_main()

        load_results_for_season(season=season)
        normalize_results_for_season(season=season)
        load_fact_for_season(season=season)

    print("[PIPELINE] Multi-season reload завершен")


if __name__ == "__main__":
    main()