-- SIMULATING POSTGRESQL LOCK QUEUE OUTAGE & LOCK TIMEOUT PROTECTION
DROP TABLE IF EXISTS migration_test;

CREATE TABLE migration_test (
    id SERIAL PRIMARY KEY,
    name TEXT
);

INSERT INTO migration_test (name) SELECT 'User ' || g FROM generate_series(1, 1000) g;

-- ============================================================================
-- SCENARIO: Lock Queue Pile-up
-- ============================================================================

-- [SESSION 1 - Simulates long-running read query / transaction holding AccessShareLock]
BEGIN;
SELECT * FROM migration_test, pg_sleep(30);
-- Keep this query running...

-- [SESSION 2 - Migration script attempts DDL requiring AccessExclusiveLock]
-- WITHOUT lock_timeout, this WAITS in line for Session 1 to finish:
ALTER TABLE migration_test ADD COLUMN phone VARCHAR(20);
-- (Session 2 is blocked)

-- [SESSION 3 - New normal application SELECT arrives]
SELECT * FROM migration_test WHERE id = 1;
-- NOTICE: SESSION 3 IS BLOCKED TOO! It is queued behind Session 2!
-- In production, this causes the connection pool to exhaust in seconds.

-- ============================================================================
-- SOLUTION: SET lock_timeout = '2s'
-- ============================================================================
-- Cancel the blocked queries, then test the fix in Session 2:
SET lock_timeout = '2s';
ALTER TABLE migration_test ADD COLUMN phone VARCHAR(20);
-- After 2 seconds, Postgres aborts the migration instead of queuing app traffic:
-- ERROR:  canceling statement due to lock timeout
