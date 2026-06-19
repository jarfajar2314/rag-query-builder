CREATE TABLE IF NOT EXISTS status_rules (
    id SERIAL PRIMARY KEY,

    name VARCHAR(150) NOT NULL,
    description TEXT,

    status_column_catalog_id INTEGER NOT NULL
        REFERENCES data_catalog(id),

    time_column_catalog_id INTEGER NOT NULL
        REFERENCES data_catalog(id),

    category_column_catalog_id INTEGER
        REFERENCES data_catalog(id),

    running_values JSONB NOT NULL DEFAULT '[]'::jsonb,
    downtime_values JSONB NOT NULL,

    expected_interval_seconds INTEGER NOT NULL,
    gap_tolerance_seconds INTEGER NOT NULL,
    minimum_downtime_seconds INTEGER NOT NULL DEFAULT 0,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
