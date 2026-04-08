-- Creating Staging Table
-- To populate the dimension tables

CREATE TABLE staging_master_data (
    serial_number BIGINT NOT NULL,
    
    facility_availability VARCHAR(255),
    type_of_purchase VARCHAR(100),
    model VARCHAR(50),
    no_of_modules INT,
    capability VARCHAR(10),
    ownership VARCHAR(50),
    workstation VARCHAR(20),
    software_version DECIMAL(3,1),
    
    first_installation_date DATE,
    warranty_status VARCHAR(50),
    warranty_end_date DATE,
    
    service_provider VARCHAR(100),
    region VARCHAR(20),
    province VARCHAR(50),
    hospital_designation VARCHAR(100),
    
    assigned_engineer VARCHAR(100),
    status VARCHAR(50),
    
    last_maintenance_visit_date DATE,
    last_maintenance_sr_no VARCHAR(50),
    last_xpertcheck_date DATE,
    last_xpertcheck_sr_no VARCHAR(50),
    
    service_ticket_if_not_operational VARCHAR(50),
    
    utilization_rate DECIMAL(10,8),
    adf_generation_date DATE,
    last_database_update DATE,
    
    total_tests INT,
    
    latitude DECIMAL(11,8),
    longitude DECIMAL(11,8),
    
    end_user_name VARCHAR(100),
    contact_number VARCHAR(20),
    email VARCHAR(255),
    
    CONSTRAINT pk_master_data PRIMARY KEY (serial_number)
) ENGINE=InnoDB;