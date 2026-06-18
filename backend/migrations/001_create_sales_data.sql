CREATE TABLE IF NOT EXISTS sales_data (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    amount NUMERIC NOT NULL,
    region VARCHAR(100),
    machine_name VARCHAR(100)
);

INSERT INTO sales_data (created_at, amount, region, machine_name)
SELECT
    timestamp '2026-06-01 00:00:00' + (random() * (interval '30 days')) AS created_at,
    floor(random() * 5000000 + 1000000)::numeric AS amount,
    (ARRAY['Jakarta', 'Bandung', 'Surabaya'])[floor(random() * 3 + 1)] AS region,
    (ARRAY['Machine A', 'Machine B', 'Machine C'])[floor(random() * 3 + 1)] AS machine_name
FROM generate_series(1, 500);