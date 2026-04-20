-- Populating the dims from stg_master_data
-- Creating values for dim_date

SET SESSION cte_max_recursion_depth = 400;

INSERT INTO dim_date (
    date_id,
    `date`,
    `year`,
    quarter,
    `month`,
    month_name,
    day_of_month
)
SELECT
    DATE_FORMAT(d, '%Y%m%d') + 0 AS date_id,
    d AS `date`,
    YEAR(d) AS `year`,
    QUARTER(d) AS quarter,
    MONTH(d) AS `month`,
    MONTHNAME(d) AS month_name,
    DAY(d) AS day_of_month
FROM (
    WITH RECURSIVE date_series AS (
        SELECT DATE('2025-01-01') AS d
        UNION ALL
        SELECT d + INTERVAL 1 DAY
        FROM date_series
        WHERE d < '2025-12-31'
    )
    SELECT d
    FROM date_series
) AS dates;

INSERT INTO dim_machine (
    serial_number,
    model,
    capability,
    no_of_modules,
    software_version,
    workstation,
    ownership,
    type_of_purchase
)
SELECT DISTINCT
    serial_number,
    model,
    capability,
    no_of_modules,
    software_version,
    workstation,
    ownership,
    type_of_purchase
FROM staging_master_data
WHERE serial_number IS NOT NULL;

INSERT INTO dim_facility (
    facility_name,
    hospital_designation,
    region,
    province,
    latitude,
    longitude,
    end_user_name,
    contact_number,
    email
)
SELECT
    facility_availability AS facility_name,
    MAX(hospital_designation),
    MAX(region),
    MAX(province),
    MAX(latitude),
    MAX(longitude),
    MAX(end_user_name),
    MAX(contact_number),
    MAX(email)
FROM staging_master_data
WHERE facility_availability IS NOT NULL
GROUP BY facility_availability;

INSERT INTO dim_engineer (engineer_name)
SELECT DISTINCT
    assigned_engineer
FROM staging_master_data
WHERE assigned_engineer IS NOT NULL
  AND assigned_engineer <> '';