-- REPRODUCING DEADLOCK IN POSTGRESQL
-- Uses accounts table from 02-lost-update (ensure accounts 1 and 2 exist):
INSERT INTO accounts (id, owner_name, balance) VALUES (2, 'David', 200.00) 
ON CONFLICT (id) DO NOTHING;

-- [SESSION 1 - Locks Account 1]
BEGIN;
UPDATE accounts SET balance = balance - 10 WHERE id = 1;
-- Lock acquired on Row 1! (Do not commit yet)

-- [SESSION 2 - Locks Account 2]
BEGIN;
UPDATE accounts SET balance = balance - 20 WHERE id = 2;
-- Lock acquired on Row 2! (Do not commit yet)

-- [SESSION 1 - Now tries to lock Account 2]
UPDATE accounts SET balance = balance + 10 WHERE id = 2;
-- SESSION 1 PAUSES (Waiting for Session 2 to release Row 2)

-- [SESSION 2 - Now tries to lock Account 1]
UPDATE accounts SET balance = balance + 20 WHERE id = 1;
-- DEADLOCK CYCLE CREATED!
-- After deadlock_timeout (default 1000ms), PostgreSQL's deadlock detector triggers:
-- ERROR:  deadlock detected
-- DETAIL: Process 1234 waits for ExclusiveLock on tuple (0,1) of relation 16384;
--         blocked by process 5678.
--         Process 5678 waits for ExclusiveLock on tuple (0,2); blocked by process 1234.
-- HINT:   See server log for query details.
