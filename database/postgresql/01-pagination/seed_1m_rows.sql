-- SEEDING 1,000,000 ROWS FOR BENCHMARKING PAGINATION
DROP TABLE IF EXISTS transactions CASCADE;

CREATE TABLE transactions (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    description TEXT,
    payload_json JSONB,
    created_at TIMESTAMPTZ NOT NULL
);

-- Generate 1,000,000 realistic transactions in ~5-10 seconds
INSERT INTO transactions (user_id, amount, description, payload_json, created_at)
SELECT 
    (random() * 10000)::int + 1,
    (random() * 500)::numeric(10, 2) + 1.00,
    'Transaction description for order ' || g,
    jsonb_build_object('source', 'mobile_app', 'merchant_id', (random() * 500)::int, 'tax_rate', 0.19),
    NOW() - (g || ' seconds')::interval
FROM generate_series(1, 1000000) g;

-- Supporting composite B-tree index for Keyset and Sorting
CREATE INDEX idx_transactions_created_id ON transactions (created_at DESC, id DESC);

VACUUM ANALYZE transactions;

SELECT count(*) AS total_rows FROM transactions;
