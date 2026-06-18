-- Drop the old catalog table because schema changed significantly
DROP TABLE IF EXISTS data_catalog;

CREATE TABLE IF NOT EXISTS data_sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    database_type VARCHAR(50) NOT NULL,
    host VARCHAR(255),
    port INTEGER,
    database_name VARCHAR(100),
    username VARCHAR(100),
    password_encrypted TEXT,
    default_schema VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS data_catalog (
    id SERIAL PRIMARY KEY,
    data_source_id INTEGER REFERENCES data_sources(id),
    schema_name VARCHAR(100),
    table_name VARCHAR(100) NOT NULL,
    column_name VARCHAR(100) NOT NULL,
    column_type VARCHAR(100),
    business_name VARCHAR(150),
    description TEXT,
    unit VARCHAR(50),
    aliases TEXT,
    is_time_column BOOLEAN DEFAULT FALSE,
    is_value_column BOOLEAN DEFAULT FALSE,
    is_category_column BOOLEAN DEFAULT FALSE,
    default_aggregation VARCHAR(50),
    default_chart VARCHAR(50),
    is_queryable BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (data_source_id, schema_name, table_name, column_name)
);

-- Seed initial data source
INSERT INTO data_sources (name, database_type, host, port, database_name, username, password_encrypted, default_schema)
VALUES ('Demo PostgreSQL', 'postgresql', 'localhost', 5432, 'rag_query_builder', 'postgres', 'postgres', 'public');

-- Re-seed catalog for sales_data
INSERT INTO data_catalog (
    data_source_id, schema_name, table_name, column_name, column_type,
    business_name, description, unit, is_time_column, is_value_column, is_category_column,
    default_chart, aliases
) VALUES
(1, 'public', 'sales_data', 'created_at', 'timestamp', 'Sales Date', 'Transaction timestamp', NULL, TRUE, FALSE, FALSE, 'line', 'date,time,transaction date'),
(1, 'public', 'sales_data', 'amount', 'numeric', 'Sales Amount', 'Total sales amount', 'IDR', FALSE, TRUE, FALSE, 'line', 'sales,revenue,amount,total sales'),
(1, 'public', 'sales_data', 'region', 'varchar', 'Sales Region', 'Region where the transaction happened', NULL, FALSE, FALSE, TRUE, 'bar', 'area,location,region'),
(1, 'public', 'sales_data', 'machine_name', 'varchar', 'Machine Name', 'Machine that produced the sale', NULL, FALSE, FALSE, TRUE, 'bar', 'machine,equipment');
