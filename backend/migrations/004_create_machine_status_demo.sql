CREATE TABLE IF NOT EXISTS machine_status (
    id BIGSERIAL PRIMARY KEY,
    recorded_at TIMESTAMPTZ NOT NULL,
    machine_name VARCHAR(100) NOT NULL,
    sta_run INTEGER NOT NULL
);
