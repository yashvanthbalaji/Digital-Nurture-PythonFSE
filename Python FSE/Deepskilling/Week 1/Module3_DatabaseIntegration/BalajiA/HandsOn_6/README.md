# HANDS-ON 6: ORM Integration — SQLAlchemy & Django ORM

**Author:**  Balaji A

## Topic

ORM Integration using SQLAlchemy and Django ORM, including Model Definition, Relationships, CRUD Operations, Sessions, Connection Pooling, and N+1 Query Optimization with `joinedload`.

## Output

> **Screenshots of the following are attached below:**
>
> <img width="1918" height="992" alt="Screenshot 2026-07-02 104212" src="https://github.com/user-attachments/assets/03d15d0a-afa9-4009-8915-3d369b79a3f7" />
<img width="1907" height="1010" alt="Screenshot 2026-07-02 104054" src="https://github.com/user-attachments/assets/a18571df-8e44-44c7-845c-9cc078fabe5e" />


* SQLAlchemy model definitions (`models.py`)
* Database tables created successfully (`college_db_orm`)
* CRUD operations (Insert, Read, Update, Delete)
* Query results displayed using SQLAlchemy ORM
* SQL query logs with `echo=True`
* N+1 query demonstration
* Optimized query using `joinedload`
* Query count comparison before and after optimization

## Result

* Successfully created ORM models matching the database schema.
* Established relationships between Department, Student, Course, Enrollment, and Professor.
* Performed CRUD operations using SQLAlchemy Session.
* Verified database changes through ORM queries.
* Identified the N+1 query problem using SQL query logs.
* Eliminated the N+1 problem using `joinedload`, reducing multiple SQL queries to a single optimized query.
* Demonstrated improved database performance and efficient ORM data retrieval.
