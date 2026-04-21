from src.ingestion.load_entity import load_single_entity


def main() -> None:
    season = 2023
    entities = ["races", "drivers", "constructors"]

    print(f"[BATCH] Начинаю batch ingestion за сезон {season}")

    for entity in entities:
        print(f"[BATCH] Загружаю entity={entity}")
        load_single_entity(season=season, entity=entity)

    print("[BATCH] Batch ingestion завершен успешно")


if __name__ == "__main__":
    main()