-- FIXING WRITE SKEW USING SERIALIZABLE SNAPSHOT ISOLATION (SSI)
-- First reset data: \i database/concurrency/01-write-skew/setup.sql

-- [SESSION 1 - Alice requests leave under SERIALIZABLE]
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT count(*) FROM doctors WHERE on_call = true;
UPDATE doctors SET on_call = false WHERE name = 'Doctor Alice';

-- [SESSION 2 - Bob requests leave under SERIALIZABLE]
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT count(*) FROM doctors WHERE on_call = true;
UPDATE doctors SET on_call = false WHERE name = 'Doctor Bob';

-- [SESSION 1 - Commits]
COMMIT; -- Success!

-- [SESSION 2 - Attempts Commit]
COMMIT;
-- ERROR:  could not serialize access due to read/write dependencies among transactions
-- DETAIL: Reason code: Canceled on identification as a pivot, during commit attempt.
-- HINT:   The transaction might succeed if retried.

-- VERIFICATION (Invariant preserved! Alice is false, Bob remains true!):
SELECT * FROM doctors;
