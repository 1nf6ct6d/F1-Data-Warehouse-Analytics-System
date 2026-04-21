from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="f1_multi_season_reload",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["f1", "dwh"],
) as dag:

    reset_dwh = BashOperator(
        task_id="reset_dwh",
        bash_command="cd /opt/project && python -m src.dwh.reset_dwh",
    )



    load_races_2021 = BashOperator(
        task_id="load_races_2021",
        bash_command="cd /opt/project && python -m src.ingestion.load_entity --entity races --season 2021",
    )
    load_races_2022 = BashOperator(
        task_id="load_races_2022",
        bash_command="cd /opt/project && python -m src.ingestion.load_entity --entity races --season 2022",
    )
    load_races_2023 = BashOperator(
        task_id="load_races_2023",
        bash_command="cd /opt/project && python -m src.ingestion.load_entity --entity races --season 2023",
    )

    normalize_races_2021 = BashOperator(
        task_id="normalize_races_2021",
        bash_command='cd /opt/project && python -c "from src.transform.normalize_races_season import normalize_races_for_season; normalize_races_for_season(2021)"',
    )
    normalize_races_2022 = BashOperator(
        task_id="normalize_races_2022",
        bash_command='cd /opt/project && python -c "from src.transform.normalize_races_season import normalize_races_for_season; normalize_races_for_season(2022)"',
    )
    normalize_races_2023 = BashOperator(
        task_id="normalize_races_2023",
        bash_command='cd /opt/project && python -c "from src.transform.normalize_races_season import normalize_races_for_season; normalize_races_for_season(2023)"',
    )

    load_dim_race_2021 = BashOperator(
        task_id="load_dim_race_2021",
        bash_command='cd /opt/project && python -c "from src.dwh.load_dim_race_season import load_dim_race_for_season; load_dim_race_for_season(2021)"',
    )
    load_dim_race_2022 = BashOperator(
        task_id="load_dim_race_2022",
        bash_command='cd /opt/project && python -c "from src.dwh.load_dim_race_season import load_dim_race_for_season; load_dim_race_for_season(2022)"',
    )
    load_dim_race_2023 = BashOperator(
        task_id="load_dim_race_2023",
        bash_command='cd /opt/project && python -c "from src.dwh.load_dim_race_season import load_dim_race_for_season; load_dim_race_for_season(2023)"',
    )


    load_drivers_2021 = BashOperator(
        task_id="load_drivers_2021",
        bash_command="cd /opt/project && python -m src.ingestion.load_entity --entity drivers --season 2021",
    )
    load_drivers_2022 = BashOperator(
        task_id="load_drivers_2022",
        bash_command="cd /opt/project && python -m src.ingestion.load_entity --entity drivers --season 2022",
    )
    load_drivers_2023 = BashOperator(
        task_id="load_drivers_2023",
        bash_command="cd /opt/project && python -m src.ingestion.load_entity --entity drivers --season 2023",
    )

    normalize_drivers_2021 = BashOperator(
        task_id="normalize_drivers_2021",
        bash_command='cd /opt/project && python -c "from src.transform.normalize_drivers_season import normalize_drivers_for_season; normalize_drivers_for_season(2021)"',
    )
    normalize_drivers_2022 = BashOperator(
        task_id="normalize_drivers_2022",
        bash_command='cd /opt/project && python -c "from src.transform.normalize_drivers_season import normalize_drivers_for_season; normalize_drivers_for_season(2022)"',
    )
    normalize_drivers_2023 = BashOperator(
        task_id="normalize_drivers_2023",
        bash_command='cd /opt/project && python -c "from src.transform.normalize_drivers_season import normalize_drivers_for_season; normalize_drivers_for_season(2023)"',
    )

    load_dim_driver_2021 = BashOperator(
        task_id="load_dim_driver_2021",
        bash_command='cd /opt/project && python -c "from src.dwh.load_dim_driver_season import load_dim_driver_for_season; load_dim_driver_for_season(2021)"',
    )
    load_dim_driver_2022 = BashOperator(
        task_id="load_dim_driver_2022",
        bash_command='cd /opt/project && python -c "from src.dwh.load_dim_driver_season import load_dim_driver_for_season; load_dim_driver_for_season(2022)"',
    )
    load_dim_driver_2023 = BashOperator(
        task_id="load_dim_driver_2023",
        bash_command='cd /opt/project && python -c "from src.dwh.load_dim_driver_season import load_dim_driver_for_season; load_dim_driver_for_season(2023)"',
    )


    load_constructors_2021 = BashOperator(
        task_id="load_constructors_2021",
        bash_command="cd /opt/project && python -m src.ingestion.load_entity --entity constructors --season 2021",
    )
    load_constructors_2022 = BashOperator(
        task_id="load_constructors_2022",
        bash_command="cd /opt/project && python -m src.ingestion.load_entity --entity constructors --season 2022",
    )
    load_constructors_2023 = BashOperator(
        task_id="load_constructors_2023",
        bash_command="cd /opt/project && python -m src.ingestion.load_entity --entity constructors --season 2023",
    )

    normalize_constructors_2021 = BashOperator(
        task_id="normalize_constructors_2021",
        bash_command='cd /opt/project && python -c "from src.transform.normalize_constructors_season import normalize_constructors_for_season; normalize_constructors_for_season(2021)"',
    )
    normalize_constructors_2022 = BashOperator(
        task_id="normalize_constructors_2022",
        bash_command='cd /opt/project && python -c "from src.transform.normalize_constructors_season import normalize_constructors_for_season; normalize_constructors_for_season(2022)"',
    )
    normalize_constructors_2023 = BashOperator(
        task_id="normalize_constructors_2023",
        bash_command='cd /opt/project && python -c "from src.transform.normalize_constructors_season import normalize_constructors_for_season; normalize_constructors_for_season(2023)"',
    )

    load_dim_constructor_2021 = BashOperator(
        task_id="load_dim_constructor_2021",
        bash_command='cd /opt/project && python -c "from src.dwh.load_dim_constructor_season import load_dim_constructor_for_season; load_dim_constructor_for_season(2021)"',
    )
    load_dim_constructor_2022 = BashOperator(
        task_id="load_dim_constructor_2022",
        bash_command='cd /opt/project && python -c "from src.dwh.load_dim_constructor_season import load_dim_constructor_for_season; load_dim_constructor_for_season(2022)"',
    )
    load_dim_constructor_2023 = BashOperator(
        task_id="load_dim_constructor_2023",
        bash_command='cd /opt/project && python -c "from src.dwh.load_dim_constructor_season import load_dim_constructor_for_season; load_dim_constructor_for_season(2023)"',
    )


    load_results_2021 = BashOperator(
        task_id="load_results_2021",
        bash_command='cd /opt/project && python -c "from src.ingestion.load_results_season import load_results_for_season; load_results_for_season(2021)"',
    )
    load_results_2022 = BashOperator(
        task_id="load_results_2022",
        bash_command='cd /opt/project && python -c "from src.ingestion.load_results_season import load_results_for_season; load_results_for_season(2022)"',
    )
    load_results_2023 = BashOperator(
        task_id="load_results_2023",
        bash_command='cd /opt/project && python -c "from src.ingestion.load_results_season import load_results_for_season; load_results_for_season(2023)"',
    )

    normalize_results_2021 = BashOperator(
        task_id="normalize_results_2021",
        bash_command='cd /opt/project && python -c "from src.transform.normalize_results_season import normalize_results_for_season; normalize_results_for_season(2021)"',
    )
    normalize_results_2022 = BashOperator(
        task_id="normalize_results_2022",
        bash_command='cd /opt/project && python -c "from src.transform.normalize_results_season import normalize_results_for_season; normalize_results_for_season(2022)"',
    )
    normalize_results_2023 = BashOperator(
        task_id="normalize_results_2023",
        bash_command='cd /opt/project && python -c "from src.transform.normalize_results_season import normalize_results_for_season; normalize_results_for_season(2023)"',
    )

    load_fact_2021 = BashOperator(
        task_id="load_fact_2021",
        bash_command='cd /opt/project && python -c "from src.dwh.load_fact_race_result_season import load_fact_for_season; load_fact_for_season(2021)"',
    )
    load_fact_2022 = BashOperator(
        task_id="load_fact_2022",
        bash_command='cd /opt/project && python -c "from src.dwh.load_fact_race_result_season import load_fact_for_season; load_fact_for_season(2022)"',
    )
    load_fact_2023 = BashOperator(
        task_id="load_fact_2023",
        bash_command='cd /opt/project && python -c "from src.dwh.load_fact_race_result_season import load_fact_for_season; load_fact_for_season(2023)"',
    )

    reset_dwh >> [load_races_2021, load_races_2022, load_races_2023]
    reset_dwh >> [load_drivers_2021, load_drivers_2022, load_drivers_2023]
    reset_dwh >> [load_constructors_2021, load_constructors_2022, load_constructors_2023]

    load_races_2021 >> normalize_races_2021 >> load_dim_race_2021
    load_races_2022 >> normalize_races_2022 >> load_dim_race_2022
    load_races_2023 >> normalize_races_2023 >> load_dim_race_2023

    load_drivers_2021 >> normalize_drivers_2021 >> load_dim_driver_2021
    load_drivers_2022 >> normalize_drivers_2022 >> load_dim_driver_2022
    load_drivers_2023 >> normalize_drivers_2023 >> load_dim_driver_2023

    load_constructors_2021 >> normalize_constructors_2021 >> load_dim_constructor_2021
    load_constructors_2022 >> normalize_constructors_2022 >> load_dim_constructor_2022
    load_constructors_2023 >> normalize_constructors_2023 >> load_dim_constructor_2023

    [
        load_dim_race_2021,
        load_dim_driver_2021,
        load_dim_constructor_2021,
    ] >> load_results_2021

    [
        load_dim_race_2022,
        load_dim_driver_2022,
        load_dim_constructor_2022,
    ] >> load_results_2022

    [
        load_dim_race_2023,
        load_dim_driver_2023,
        load_dim_constructor_2023,
    ] >> load_results_2023

    load_results_2021 >> normalize_results_2021 >> load_fact_2021
    load_results_2022 >> normalize_results_2022 >> load_fact_2022
    load_results_2023 >> normalize_results_2023 >> load_fact_2023