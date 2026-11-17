-- FIXING LOST UPDATE VIA OPTIMISTIC LOCKING (Version check)
-- Reset data: \i database/concurrency/02-lost-update/setup.sql

-- [SESSION 1 - User A reads]
SELECT balance, version FROM accounts WHERE id = 1; -- bal=100, version=1

-- [SESSION 2 - User B reads concurrently]
SELECT balance, version FROM accounts WHERE id = 1; -- bal=100, version=1

-- [SESSION 1 - User A updates with version check]
UPDATE accounts 
SET balance = 150.00, version = version + 1 
WHERE id = 1 AND version = 1;
-- UPDATE 1 (Success!)

-- [SESSION 2 - User B attempts update with stale version=1]
UPDATE accounts 
SET balance = 120.00, version = version + 1 
WHERE id = 1 AND version = 1;
-- UPDATE 0 (Rows affected: 0!)
-- Application detects 0 rows updated, knows a concurrent modification occurred, and retries!
