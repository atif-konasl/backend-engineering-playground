-- REPRODUCING WRITE SKEW UNDER REPEATABLE READ
-- Open TWO terminal windows or two database query tabs (Session 1 & Session 2).

-- [SESSION 1 - Alice requests leave]
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT count(*) FROM doctors WHERE on_call = true;
-- Output: 2. Alice sees there is at least 1 other doctor on call.

-- [SESSION 2 - Bob concurrently requests leave]
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT count(*) FROM doctors WHERE on_call = true;
-- Output: 2. Bob also sees there is at least 1 other doctor on call.

-- [SESSION 1 - Alice signs off]
UPDATE doctors SET on_call = false WHERE name = 'Doctor Alice';

-- [SESSION 2 - Bob signs off]
UPDATE doctors SET on_call = false WHERE name = 'Doctor Bob';

-- [SESSION 1 - Alice commits]
COMMIT; -- Success!

-- [SESSION 2 - Bob commits]
COMMIT; -- Success! (NO CONFLICT DETECTED BY REPEATABLE READ!)

-- VERIFICATION (Invariant violated! 0 doctors on call!):
SELECT * FROM doctors;
