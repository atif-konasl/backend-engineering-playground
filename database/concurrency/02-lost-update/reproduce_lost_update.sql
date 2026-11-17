-- REPRODUCING LOST UPDATE IN READ COMMITTED
-- Initial balance: $100.
-- User A deposits $50 (expects $150).
-- User B deposits $20 (expects $120).
-- Combined total should be $170.

-- [SESSION 1 - User A reads balance]
BEGIN;
SELECT balance FROM accounts WHERE id = 1; -- reads 100.00
-- Application computes: 100 + 50 = 150

-- [SESSION 2 - User B reads balance concurrently]
BEGIN;
SELECT balance FROM accounts WHERE id = 1; -- reads 100.00
-- Application computes: 100 + 20 = 120

-- [SESSION 1 - User A writes back $150]
UPDATE accounts SET balance = 150.00 WHERE id = 1;
COMMIT;

-- [SESSION 2 - User B writes back $120]
UPDATE accounts SET balance = 120.00 WHERE id = 1;
COMMIT;

-- VERIFICATION:
SELECT * FROM accounts WHERE id = 1;
-- Balance is $120.00! User A's $50 deposit was silently LOST!
