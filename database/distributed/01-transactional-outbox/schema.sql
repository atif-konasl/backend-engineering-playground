-- TRANSACTIONAL OUTBOX PATTERN PLAYGROUND
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS outbox_events CASCADE;

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INT NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'CREATED',
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

CREATE TABLE outbox_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(50) NOT NULL,
    aggregate_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- ============================================================================
-- 1. ATOMIC BUSINESS INSERT + OUTBOX EVENT (Guarantees No Dual-Write Bug)
-- ============================================================================
BEGIN;

WITH new_order AS (
    INSERT INTO orders (user_id, total_amount)
    VALUES (42, 199.99)
    RETURNING id, user_id, total_amount, status
)
INSERT INTO outbox_events (aggregate_type, aggregate_id, event_type, payload)
SELECT 
    'Order',
    id::text,
    'OrderCreated',
    jsonb_build_object('order_id', id, 'user_id', user_id, 'amount', total_amount, 'status', status)
FROM new_order;

COMMIT;

-- Verify both were committed atomically:
SELECT * FROM orders;
SELECT * FROM outbox_events;

-- ============================================================================
-- 2. POLLING WORKER CONSUMING OUTBOX WITH SKIP LOCKED
-- (Allows multiple parallel worker threads to poll without contention)
-- ============================================================================
BEGIN;

-- Lock and retrieve next 10 unpublished events
WITH claimed_events AS (
    SELECT id, payload
    FROM outbox_events
    ORDER BY created_at ASC
    LIMIT 10
    FOR UPDATE SKIP LOCKED
)
-- After simulating publishing to Kafka:
DELETE FROM outbox_events
WHERE id IN (SELECT id FROM claimed_events);

COMMIT;
