CREATE TABLE IF NOT EXISTS data_catalog (
    id SERIAL PRIMARY KEY,
    database_type VARCHAR(50) NOT NULL,
    database_name VARCHAR(100),
    schema_name VARCHAR(100) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    column_name VARCHAR(100) NOT NULL,
    column_type VARCHAR(50),
    business_name VARCHAR(150),
    description TEXT,
    unit VARCHAR(50),
    is_time_column BOOLEAN DEFAULT FALSE,
    is_value_column BOOLEAN DEFAULT FALSE,
    is_category_column BOOLEAN DEFAULT FALSE,
    default_chart VARCHAR(50),
    aliases TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO data_catalog (
    database_type, database_name, schema_name, table_name,
    column_name, column_type, business_name, description,
    unit, is_time_column, is_value_column, is_category_column,
    default_chart, aliases
) VALUES
('postgresql', 'rag_query_builder', 'public', 'sales_data', 'created_at', 'timestamp', 'Sales Date', 'Transaction timestamp', NULL, TRUE, FALSE, FALSE, 'line', 'date,time,transaction date'),
('postgresql', 'rag_query_builder', 'public', 'sales_data', 'amount', 'numeric', 'Sales Amount', 'Total sales amount', 'IDR', FALSE, TRUE, FALSE, 'line', 'sales,revenue,amount,total sales'),
('postgresql', 'rag_query_builder', 'public', 'sales_data', 'region', 'varchar', 'Sales Region', 'Region where the transaction happened', NULL, FALSE, FALSE, TRUE, 'bar', 'area,location,region'),
('postgresql', 'rag_query_builder', 'public', 'sales_data', 'machine_name', 'varchar', 'Machine Name', 'Machine that produced the sale', NULL, FALSE, FALSE, TRUE, 'bar', 'machine,equipment');
