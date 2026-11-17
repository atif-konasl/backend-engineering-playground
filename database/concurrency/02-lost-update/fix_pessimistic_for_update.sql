-- FIXING LOST UPDATE VIA PESSIMISTIC LOCKING (FOR UPDATE)
-- Reset data: \i database/concurrency/02-lost-update/setup.sql

-- [SESSION 1 - User A acquires row lock]
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
-- Reads 100.00. Lock acquired!

-- [SESSION 2 - User B attempts to read with FOR UPDATE]
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
-- SESSION 2 PAUSES AND WAITS! (Blocked by Session 1)

-- [SESSION 1 - User A writes and commits]
UPDATE accounts SET balance = 150.00 WHERE id = 1;
COMMIT;

-- [SESSION 2 - Instantly unblocks upon Session 1's commit!]
-- Session 2 receives the NEW balance: 150.00!
-- Application calculates: 150 + 20 = 170.00
UPDATE accounts SET balance = 170.00 WHERE id = 1;
COMMIT;

-- VERIFICATION:
SELECT * FROM accounts WHERE id = 1;
-- Balance is $170.00! Correct!
