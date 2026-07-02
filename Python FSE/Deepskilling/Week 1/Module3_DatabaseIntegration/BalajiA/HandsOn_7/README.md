# HANDS-ON 7: Migrations & Versioning — Alembic and Django Migrations

**Author:** Balaji A

## Topic

Migration Concepts, Alembic for SQLAlchemy, Django Migrations, Migration History, Version Control, and Rollback Strategies.

## Output

> **Screenshots of the following are attached below:**
<img width="1917" height="1076" alt="Screenshot 2026-07-02 102730" src="https://github.com/user-attachments/assets/fb221198-d115-46dd-96f3-21a5c69e1754" />
<img width="1828" height="471" alt="Screenshot 2026-07-02 103048" src="https://github.com/user-attachments/assets/156125f5-d262-4f7c-8e9c-164c459e0c9a" />

<img width="1223" height="790" alt="Screenshot 2026-07-02 103523" src="https://github.com/user-attachments/assets/a9e97d55-57bd-4627-b7a0-41222f0562e6" />
<img width="1875" height="1030" alt="Screenshot 2026-07-02 103333" src="https://github.com/user-attachments/assets/83c250c6-08dd-4d79-9e79-82dc63e1952e" />
<img width="1915" height="999" alt="Screenshot 2026-07-02 103141" src="https://github.com/user-attachments/assets/459204bf-8a29-4470-99c2-f394f76f4f1f" />


* Alembic initialization (`alembic init migrations`)
* Baseline migration generation
* `alembic upgrade head` output
* `alembic_version` table in database
* Migration for `is_active` column
* Migration for `CourseSchedule` table
* `alembic history --verbose` output
* Rollback using `alembic downgrade -1`
* Full rollback using `alembic downgrade base`
* Re-apply migration using `alembic upgrade head`

## Result

* Successfully configured Alembic for schema versioning.
* Generated and applied the initial migration from SQLAlchemy models.
* Added a new column and a new table using incremental migrations.
* Verified migration history and version tracking.
* Practised safe rollback using downgrade commands.
* Restored the latest schema successfully after rollback.
