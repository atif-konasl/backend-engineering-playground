-- SIMULATING CONCURRENT WORKERS WITH SKIP LOCKED
-- Demonstrates building lock-free job queues directly in PostgreSQL.

-- [SESSION 1 - Worker 1 claims 2 jobs]
BEGIN;
SELECT id, payload
FROM job_queue
WHERE status = 'PENDING'
ORDER BY id ASC
LIMIT 2
FOR UPDATE SKIP LOCKED;
-- Worker 1 receives Job 1 and Job 2! (Rows are now locked by Worker 1).
-- DO NOT COMMIT YET.

-- [SESSION 2 - Worker 2 polls concurrently]
BEGIN;
SELECT id, payload
FROM job_queue
WHERE status = 'PENDING'
ORDER BY id ASC
LIMIT 2
FOR UPDATE SKIP LOCKED;
-- NOTICE: Worker 2 DOES NOT BLOCK!
-- Worker 2 automatically SKIPS rows 1 and 2 and receives Job 3 and Job 4!

-- [SESSION 1 - Worker 1 marks jobs done and commits]
UPDATE job_queue SET status = 'COMPLETED', locked_by = 'Worker 1' WHERE id IN (1, 2);
COMMIT;

-- [SESSION 2 - Worker 2 marks jobs done and commits]
UPDATE job_queue SET status = 'COMPLETED', locked_by = 'Worker 2' WHERE id IN (3, 4);
COMMIT;

-- VERIFICATION:
SELECT * FROM job_queue ORDER BY id;
