-- INSPECTING POSTGRESQL MVCC SYSTEM COLUMNS (xmin, xmax, ctid)
DROP TABLE IF EXISTS mvcc_demo;

CREATE TABLE mvcc_demo (
    id SERIAL PRIMARY KEY,
    val TEXT
);

-- 1. Insert row in Transaction A
INSERT INTO mvcc_demo (val) VALUES ('Version 1');

-- Inspect hidden system columns:
SELECT ctid, xmin, xmax, id, val FROM mvcc_demo;
-- Output shows ctid=(0,1), xmin=<insert_xid>, xmax=0 (active row)

-- 2. Open an update transaction
BEGIN;
SELECT txid_current(); -- note current transaction ID
UPDATE mvcc_demo SET val = 'Version 2' WHERE id = 1;

-- Notice ctid changed! Postgres created a NEW tuple version on disk:
SELECT ctid, xmin, xmax, id, val FROM mvcc_demo;
COMMIT;

-- 3. To see the dead tuple from disk before VACUUM, install pageinspect:
CREATE EXTENSION IF NOT EXISTS pageinspect;
SELECT lp, t_ctid, t_xmin, t_xmax, t_data 
FROM heap_page_items(get_raw_page('mvcc_demo', 0));
-- You will see BOTH Version 1 and Version 2 stored side-by-side in disk page 0!
