-- Setup: Account balance for Lost Update simulation
DROP TABLE IF EXISTS accounts;

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    owner_name VARCHAR(100) NOT NULL,
    balance NUMERIC(12, 2) NOT NULL DEFAULT 100.00,
    version INT NOT NULL DEFAULT 1
);

INSERT INTO accounts (owner_name, balance, version) VALUES
    ('Charlie', 100.00, 1);

SELECT * FROM accounts;
