# HANDS-ON 7: Migrations & Versioning — Alembic and Django Migrations

**Author:** Balaji A

## Topic

Migration Concepts, Alembic for SQLAlchemy, Django Migrations, Migration History, Version Control, and Rollback Strategies.

## Output

> **Screenshots of the following are attached below:**

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
