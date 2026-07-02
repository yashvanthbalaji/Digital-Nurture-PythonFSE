# HANDS-ON 4: Query Optimisation — Indexes, EXPLAIN & the N+1 Problem

**Author:** Balaji A

## Topic

Query Optimisation using Indexes, EXPLAIN, Query Plans, and the N+1 Problem.

## Output

> **Screenshots of the following are attached below:**

* Baseline `EXPLAIN` query plan (before indexing)
* Index creation statements
* Updated `EXPLAIN` query plan (after indexing)
* Python output demonstrating the N+1 problem
* Python output after optimization using a single `JOIN`
* Query count and execution time comparison

## Result

* Successfully analyzed the query execution plan using `EXPLAIN`.
* Created B-Tree, Composite UNIQUE, and Partial indexes to improve database performance.
* Observed improved query execution plans after indexing.
* Demonstrated the N+1 query problem and resolved it using a single `JOIN` query.
* Reduced database round-trips significantly while returning the same results.
* Verified that query optimization improves database efficiency and scalability.
