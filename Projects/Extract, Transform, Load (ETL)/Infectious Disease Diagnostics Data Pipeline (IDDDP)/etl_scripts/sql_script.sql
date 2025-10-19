CREATE TABLE patients(
	patient_id VARCHAR(10) PRIMARY KEY,
	name VARCHAR(50) NULL,
	age INT NULL,
	gender VARCHAR(10) NULL,
	city VARCHAR(50) NULL,
	contact VARCHAR(15) NULL
);

CREATE TABLE lab_results(
	results_id SERIAL PRIMARY KEY,
	patient_id VARCHAR(10) REFERENCES patients(patient_id),
	test_type VARCHAR(10) NULL,
	result VARCHAR(10) NULL,
	ct_value NUMERIC(3,1) NULL,
	test_date DATE NULL
);

CREATE TABLE maintenance_logs(
	maintenance_id SERIAL PRIMARY KEY,
	device_id VARCHAR(10) NULL,
	service_date DATE NULL,
	engineer VARCHAR(25) NULL,
	status VARCHAR(15) NULL
);
	
-- SELECT * FROM patients;
-- SELECT * FROM lab_results;
-- SELECT * FROM maintenance_logs;