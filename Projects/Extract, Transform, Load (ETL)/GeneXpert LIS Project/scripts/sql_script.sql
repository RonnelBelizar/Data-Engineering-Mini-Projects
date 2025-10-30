CREATE DATABASE genexpert_lis;
USE genexpert_lis;

CREATE TABLE patients(
	patient_id INT PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    birth_date DATE,
    gender CHAR(1),
    contact_number VARCHAR(20));
    
CREATE TABLE medtechs(
	medtech_id INT PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    license_number VARCHAR(10));
    
CREATE TABLE test_records(
	test_id SERIAL PRIMARY KEY,
    test_date DATE,
    sample_type VARCHAR(20),
    test_type VARCHAR(20),
    status VARCHAR(50),
    result VARCHAR(10),
    time_completed DATETIME DEFAULT CURRENT_TIMESTAMP,
    medtech_id INT,
    patient_id INT,
    FOREIGN KEY (medtech_id) references medtechs(medtech_id),
    FOREIGN KEY (patient_id) references patients(patient_id)
    );

-- SELECT * FROM test_records;
-- SELECT * FROM medtechs;
-- SELECT * FROM patients;

CREATE VIEW test_records_view AS
SELECT
	t.test_id,
    t.patient_id,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    t.sample_type,
    t.test_type,
    t.status,
    t.result,
    CONCAT(m.first_name, ' ', m.last_name) AS medtech,
    t.time_completed AS date_and_time
FROM test_records t
JOIN patients p
	ON t.patient_id = p.patient_id
JOIN medtechs m
	ON t.medtech_id = m.medtech_id;

SELECT * FROM test_records_view
ORDER BY test_id;
