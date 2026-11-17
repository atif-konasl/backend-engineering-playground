-- PAGINATION BENCHMARK: OFFSET VS KEYSET VS DEFERRED JOIN
-- Ensure transactions table has 1M rows from seed_1m_rows.sql

-- ============================================================================
-- 1. STANDARD OFFSET AT PAGE 10,000 (OFFSET 200,000)
-- Notice: buffers hit/read count and actual execution time!
-- ============================================================================
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, user_id, amount, description, payload_json, created_at
FROM transactions
ORDER BY created_at DESC, id DESC
LIMIT 20 OFFSET 200000;


-- ============================================================================
-- 2. KEYSET (SEEK METHOD) AT EQUIVALENT POSITION
-- We capture a realistic cursor from around offset 200,000:
-- ============================================================================
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, user_id, amount, description, payload_json, created_at
FROM transactions
WHERE (created_at, id) < (NOW() - interval '200000 seconds', 800000)
ORDER BY created_at DESC, id DESC
LIMIT 20;


-- ============================================================================
-- 3. DEFERRED JOIN (LATE ROW LOOKUP) AT PAGE 10,000 (OFFSET 200,000)
-- Slices only thin index first, then fetches heavy payload for 20 rows:
-- ============================================================================
EXPLAIN (ANALYZE, BUFFERS)
SELECT t.id, t.user_id, t.amount, t.description, t.payload_json, t.created_at
FROM transactions t
JOIN (
    SELECT id
    FROM transactions
    ORDER BY created_at DESC, id DESC
    LIMIT 20 OFFSET 200000
) page ON t.id = page.id
ORDER BY t.created_at DESC, t.id DESC;
