CREATE TABLE IF NOT EXISTS srv_driver_points
(
    driver_id String,
    given_name String,
    family_name String,
    nationality String,
    total_points Float64
)
ENGINE = MergeTree
ORDER BY (total_points, driver_id);

CREATE TABLE IF NOT EXISTS srv_constructor_points
(
    constructor_id String,
    constructor_name String,
    nationality String,
    total_points Float64
)
ENGINE = MergeTree
ORDER BY (total_points, constructor_id);