# Backend Engineering Playground

An interactive collection of runnable simulations designed to help engineers master core backend concepts and prepare for senior/staff technical interviews.

Instead of reading abstract explanations about race conditions, deadlocks, write skew, or pagination cliffs, you can spin up an isolated environment, run reproducible scripts, and observe engine metrics and concurrency conflicts directly.

---

## Quickstart

```bash
# 1. Start isolated database infrastructure (Postgres 16 + Redis 7)
docker compose up -d

# 2. Connect to PostgreSQL interactive prompt
make psql
# Or: psql "postgres://postgres:postgrespassword@localhost:5432/playground"
```

---

## Interactive Simulations Index

### 1. Database Concurrency & Transactions
| Lab | Description | Runnable Script |
| :--- | :--- | :--- |
| **Write Skew & SSI** | Reproducing the "Doctors on Call" anomaly under `REPEATABLE READ` and proving how `SERIALIZABLE` (SSI) catches the dependency cycle. | `database/concurrency/01-write-skew/` |
| **Lost Updates & Locking** | Simulating concurrent balance increments, observing the lost update, and verifying fixes with Optimistic versioning vs `SELECT FOR UPDATE`. | `database/concurrency/02-lost-update/` |
| **Lock-Free Job Queue** | Simulating multiple concurrent workers polling the same table without blocking using `FOR UPDATE SKIP LOCKED`. | `database/concurrency/03-skip-locked-queue/` |
| **Deadlock Reproduction** | Triggering an intentional circular lock wait and observing PostgreSQL's automatic deadlock detector aborting one transaction. | `database/concurrency/04-deadlock-simulation/` |

---

### 2. PostgreSQL Storage & Query Performance
| Lab | Description | Runnable Script |
| :--- | :--- | :--- |
| **Pagination Benchmarks** | Seeding 1,000,000 realistic rows and running `EXPLAIN (ANALYZE, BUFFERS)` to compare `OFFSET 200,000` vs `Keyset Seek` vs `Deferred Joins`. ([Deep Dive Breakdown](./database/postgresql/01-pagination/explain_analyze_offset_deep_dive.md)) | `database/postgresql/01-pagination/` |
| **MVCC Internals** | Inspecting hidden system columns (`xmin`, `xmax`, `ctid`) and observing how `ROLLBACK` makes tuples invisible instantly without disk deletes. | `database/postgresql/02-mvcc-internals/` |
| **Zero-Downtime Migrations** | Reproducing the production lock queue pile-up (`AccessExclusiveLock` blocking reads) and testing `SET lock_timeout = '2s'` protection. | `database/postgresql/03-zero-downtime-migrations/` |
| **Partition Pruning** | Setting up declarative range partitions and proving with `EXPLAIN` how unqueried partitions are completely eliminated from disk I/O. | `database/postgresql/04-partition-pruning/` |

---

### 3. Distributed Scaling & Consistency
| Lab | Description | Runnable Script |
| :--- | :--- | :--- |
| **Transactional Outbox** | Eliminating the Dual-Write bug by atomically committing business entities and outbox events, consumed via `SKIP LOCKED`. | `database/distributed/01-transactional-outbox/` |
