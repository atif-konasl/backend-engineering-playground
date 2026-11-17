-- Setup: Doctors on Call (Invariant: at least 1 doctor must be on call)
DROP TABLE IF EXISTS doctors;

CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    on_call BOOLEAN NOT NULL DEFAULT true
);

INSERT INTO doctors (name, on_call) VALUES
    ('Doctor Alice', true),
    ('Doctor Bob', true);

SELECT * FROM doctors;
