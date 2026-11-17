-- DECLARATIVE PARTITIONING & PARTITION PRUNING EXPERIMENT
DROP TABLE IF EXISTS orders_partitioned CASCADE;

CREATE TABLE orders_partitioned (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    user_id INT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    created_at DATE NOT NULL,
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Create 3 child monthly partitions
CREATE TABLE orders_2026_01 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE orders_2026_02 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

CREATE TABLE orders_2026_03 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

-- Seed sample rows into all partitions
INSERT INTO orders_partitioned (user_id, amount, created_at) VALUES
    (101, 50.00, '2026-01-15'),
    (102, 75.00, '2026-02-10'),
    (103, 120.00, '2026-03-05');

-- ============================================================================
-- VERIFY PARTITION PRUNING
-- ============================================================================
EXPLAIN (ANALYZE, COSTS OFF)
SELECT * FROM orders_partitioned 
WHERE created_at BETWEEN '2026-02-01' AND '2026-02-28';
-- Notice in output: Postgres executes Seq Scan on 'orders_2026_02' ONLY!
-- Partitions orders_2026_01 and orders_2026_03 are completely PRUNED (0 cost, 0 disk I/O).
