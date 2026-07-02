# HANDS-ON 4: Query Optimisation — Indexes, EXPLAIN & the N+1 Problem

**Author:** Balaji A

## Topic

Query Optimisation using Indexes, EXPLAIN, Query Plans, and the N+1 Problem.

## Output

> **Screenshots of the following are attached below:**
>
<img width="1868" height="945" alt="Screenshot 2026-07-02 111119" src="https://github.com/user-attachments/assets/cc48e2b5-2506-488b-9c18-01ac7f8864bf" />
<img width="1720" height="1002" alt="Screenshot 2026-07-02 110953" src="https://github.com/user-attachments/assets/f3890465-8e48-464d-8915-a90532f0965a" />
<img width="1544" height="1026" alt="Screenshot 2026-07-02 110917" src="https://github.com/user-attachments/assets/c4abcbf5-e04a-4cd2-8d4b-480257723d04" />
<img width="1497" height="1050" alt="Screenshot 2026-07-02 110901" src="https://github.com/user-attachments/assets/8e1cec7c-5b52-4e64-8971-77d4c326c801" />


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
