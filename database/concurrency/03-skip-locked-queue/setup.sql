-- Setup: High-Throughput Job Queue
DROP TABLE IF EXISTS job_queue;

CREATE TABLE job_queue (
    id SERIAL PRIMARY KEY,
    payload TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    locked_by VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

INSERT INTO job_queue (payload) VALUES
    ('Send Welcome Email to User 1'),
    ('Generate Invoice #1024'),
    ('Resize Profile Photo 88'),
    ('Notify Slack Channel #sales'),
    ('Sync Stripe Webhook evt_99');

SELECT * FROM job_queue;
