CREATE OR REPLACE VIEW vw_race_results AS
SELECT
    r.season,
    r.round_number,
    r.race_name,
    r.race_date,
    d.driver_id,
    d.given_name,
    d.family_name,
    c.constructor_name,
    f.grid_position,
    f.finish_position,
    f.position_text,
    f.points,
    f.status,
    f.fastest_lap_time,
    f.fastest_lap_avg_speed
FROM fact_race_result f
JOIN dim_race r
    ON f.race_sk = r.race_sk
JOIN dim_driver d
    ON f.driver_sk = d.driver_sk
JOIN dim_constructor c
    ON f.constructor_sk = c.constructor_sk;


CREATE OR REPLACE VIEW vw_driver_points AS
SELECT
    d.driver_id,
    d.given_name,
    d.family_name,
    d.nationality,
    SUM(f.points) AS total_points
FROM fact_race_result f
JOIN dim_driver d
    ON f.driver_sk = d.driver_sk
GROUP BY
    d.driver_id,
    d.given_name,
    d.family_name,
    d.nationality;


CREATE OR REPLACE VIEW vw_constructor_points AS
SELECT
    c.constructor_id,
    c.constructor_name,
    c.nationality,
    SUM(f.points) AS total_points
FROM fact_race_result f
JOIN dim_constructor c
    ON f.constructor_sk = c.constructor_sk
GROUP BY
    c.constructor_id,
    c.constructor_name,
    c.nationality;


CREATE OR REPLACE VIEW vw_driver_podiums AS
SELECT
    d.driver_id,
    d.given_name,
    d.family_name,
    COUNT(*) AS podiums
FROM fact_race_result f
JOIN dim_driver d
    ON f.driver_sk = d.driver_sk
WHERE f.finish_position IN (1, 2, 3)
GROUP BY
    d.driver_id,
    d.given_name,
    d.family_name;