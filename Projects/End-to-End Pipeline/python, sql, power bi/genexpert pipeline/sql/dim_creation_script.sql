-- Creating the GeneXpert Project Schema
-- Creating database

create database genexpert_project_db;
use genexpert_project_db;

-- Creating dimension Tables
-- For this project, there are 4 main dimension tables: dim_date, dim_machine, dim_engineer, dim_facility

CREATE TABLE dim_machine (
    machine_id INT AUTO_INCREMENT PRIMARY KEY,
    serial_number BIGINT NOT NULL UNIQUE,

    model VARCHAR(50),
    capability VARCHAR(10),
    no_of_modules INT,
    software_version DECIMAL(3,1),

    workstation VARCHAR(50),
    ownership VARCHAR(50),
    type_of_purchase VARCHAR(100)
);

CREATE TABLE dim_facility (
    facility_id INT AUTO_INCREMENT PRIMARY KEY,

    facility_name VARCHAR(255),
    hospital_designation VARCHAR(100),

    region VARCHAR(50),
    province VARCHAR(50),
    latitude DECIMAL(11,8),
    longitude DECIMAL(11,8),

    end_user_name VARCHAR(100),
    contact_number VARCHAR(30),
    email VARCHAR(255)
);

CREATE TABLE dim_engineer (
    engineer_id INT AUTO_INCREMENT PRIMARY KEY,
    engineer_name VARCHAR(100)
);

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,     -- YYYYMMDD
    date DATE NOT NULL,

    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    day_of_month INT
);