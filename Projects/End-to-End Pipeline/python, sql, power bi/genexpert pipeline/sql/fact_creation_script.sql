-- Creating a fact table

CREATE TABLE fact_machine_daily_tests (
    date_id INT NOT NULL,
    machine_id INT NOT NULL,
    facility_id INT NOT NULL,
    engineer_id INT NOT NULL,

    tests_mtb INT DEFAULT 0,
    tests_hiv INT DEFAULT 0,
    tests_ct_ng INT DEFAULT 0,
    tests_sars_cov INT DEFAULT 0,

    total_tests INT NOT NULL,
    theoretical_capacity INT NOT NULL,
    utilization_rate DECIMAL(5,3) NOT NULL,

    -- Composite PK enforces grain
    PRIMARY KEY (date_id, machine_id, facility_id),

    -- Foreign keys
    CONSTRAINT fk_fact_date
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id),

    CONSTRAINT fk_fact_machine
        FOREIGN KEY (machine_id) REFERENCES dim_machine(machine_id),

    CONSTRAINT fk_fact_facility
        FOREIGN KEY (facility_id) REFERENCES dim_facility(facility_id),

    CONSTRAINT fk_fact_engineer
        FOREIGN KEY (engineer_id) REFERENCES dim_engineer(engineer_id)
);