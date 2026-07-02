-- ============================================================
-- Digital Nurture 5.0 | Module 3: Database Integration
-- Hands-On 3: Advanced SQL - Subqueries, Views & Transactions
-- Name   : Balaji A
-- ============================================================

USE college_db;

-- TASK 1: Subqueries

-- Step 35
SELECT s.student_id,
       CONCAT(s.first_name, ' ', s.last_name) AS student_name,
       COUNT(e.course_id) AS total_courses_enrolled
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.course_id) > (
    SELECT AVG(enrollment_count)
    FROM (
        SELECT student_id, COUNT(course_id) AS enrollment_count
        FROM enrollments
        GROUP BY student_id
    ) AS avg_table
);

-- Step 36
SELECT c.course_id,
       c.course_name,
       c.course_code
FROM courses c
WHERE EXISTS (
    SELECT 1 FROM enrollments e
    WHERE e.course_id = c.course_id
)
AND NOT EXISTS (
    SELECT 1 FROM enrollments e
    WHERE e.course_id = c.course_id
    AND e.grade != 'A'
);

-- Step 37
SELECT p.professor_id,
       p.prof_name,
       p.department_id,
       p.salary
FROM professors p
WHERE p.salary = (
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
);

-- Step 38
SELECT dept_avg.department_id,
       d.dept_name,
       dept_avg.average_salary
FROM (
    SELECT department_id,
           ROUND(AVG(salary), 2) AS average_salary
    FROM professors
    GROUP BY department_id
) AS dept_avg
INNER JOIN departments d ON dept_avg.department_id = d.department_id
WHERE dept_avg.average_salary > 85000;


-- TASK 2: Creating and Using Views

-- Step 39
CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    d.dept_name                             AS department,
    COUNT(e.course_id)                      AS courses_enrolled,
    ROUND(
        AVG(
            CASE e.grade
                WHEN 'A' THEN 4
                WHEN 'B' THEN 3
                WHEN 'C' THEN 2
                WHEN 'D' THEN 1
                WHEN 'F' THEN 0
                ELSE NULL
            END
        ), 2
    )                                       AS gpa
FROM students s
INNER JOIN departments d ON s.department_id = d.department_id
INNER JOIN enrollments e ON s.student_id    = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

-- Step 40
CREATE VIEW vw_course_stats AS
SELECT c.course_name,c.course_code, COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(
        AVG(
            CASE e.grade
                WHEN 'A' THEN 4
                WHEN 'B' THEN 3
                WHEN 'C' THEN 2
                WHEN 'D' THEN 1
                WHEN 'F' THEN 0
                ELSE NULL
            END
        ), 2
    )AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

-- Step 41
SELECT *
FROM vw_student_enrollment_summary
WHERE gpa > 3.0;

SELECT * FROM vw_course_stats;

-- Step 42
-- Attempting UPDATE through vw_student_enrollment_summary:
-- UPDATE vw_student_enrollment_summary SET department = 'Civil' WHERE student_id = 1;
-- Result: ERROR - View is not updatable
--
-- Why multi-table views are not updatable:
-- vw_student_enrollment_summary joins 3 tables (students, departments, enrollments)
-- and uses GROUP BY with aggregate functions (COUNT, AVG).
-- MySQL cannot determine which base table row to update when:
--   1. The view spans multiple tables using JOIN
--   2. The view uses GROUP BY or aggregate functions
-- Hence MySQL restricts any INSERT or UPDATE on such views.

-- Step 43
DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;

CREATE VIEW vw_student_enrollment_summary AS
SELECT student_id,
       first_name,
       last_name,
       email,
       department_id,
       enrollment_year
FROM students
WHERE enrollment_year = 2022
WITH CHECK OPTION;

SELECT * FROM vw_student_enrollment_summary;

-- Test 1: This should FAIL - enrollment_year 2020 is outside view's WHERE
-- INSERT INTO vw_student_enrollment_summary
--     (first_name, last_name, email, department_id, enrollment_year)
-- VALUES ('Test', 'User', 'test@college.edu', 1, 2020);

-- Test 2: This should PASS - enrollment_year 2022 is inside view's WHERE
-- INSERT INTO vw_student_enrollment_summary
--     (first_name, last_name, email, department_id, enrollment_year)
-- VALUES ('Allowed', 'Student', 'allowed@college.edu', 1, 2022);


-- TASK 3: Stored Procedures and Transactions
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CREATE TABLE IF NOT EXISTS department_transfer_log (
    log_id           INT PRIMARY KEY AUTO_INCREMENT,
    student_id       INT      NOT NULL,
    old_department   INT      NOT NULL,
    new_department   INT      NOT NULL,
    transferred_on   DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Step 44
DELIMITER $$

CREATE PROCEDURE sp_enroll_student(
    IN p_student_id      INT,
    IN p_course_id       INT,
    IN p_enrollment_date DATE
)
BEGIN
    DECLARE already_enrolled INT DEFAULT 0;

    SELECT COUNT(*) INTO already_enrolled
    FROM enrollments
    WHERE student_id = p_student_id
    AND   course_id  = p_course_id;

    IF already_enrolled > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Student is already enrolled in this course!';
    ELSE
        INSERT INTO enrollments (student_id, course_id, enrollment_date)
        VALUES (p_student_id, p_course_id, p_enrollment_date);
        SELECT 'Enrollment successful!' AS result;
    END IF;
END $$

DELIMITER ;

-- New enrollment - should pass
CALL sp_enroll_student(9, 1, '2024-07-01');

-- Duplicate enrollment - should fail with error
-- CALL sp_enroll_student(1, 1, '2024-07-01');

-- Step 45
DELIMITER $$

CREATE PROCEDURE sp_transfer_student(
    IN p_student_id  INT,
    IN p_new_dept_id INT
)
BEGIN
    DECLARE old_dept_id INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Transaction failed! Changes have been rolled back.' AS result;
    END;

    SELECT department_id INTO old_dept_id
    FROM students
    WHERE student_id = p_student_id;

    START TRANSACTION;

        UPDATE students
        SET department_id = p_new_dept_id
        WHERE student_id  = p_student_id;

        INSERT INTO department_transfer_log (student_id, old_department, new_department)
        VALUES (p_student_id, old_dept_id, p_new_dept_id);

    COMMIT;
    SELECT 'Student transferred successfully!' AS result;
END $$

DELIMITER ;

CALL sp_transfer_student(2, 3);

SELECT student_id, first_name, department_id FROM students  WHERE student_id = 2;
SELECT * FROM department_transfer_log;

-- Step 46
CALL sp_transfer_student(3, 999);

SELECT student_id, first_name, department_id FROM students WHERE student_id = 3;

-- Step 47
START TRANSACTION;

    INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
    VALUES (9, 2, '2024-07-01', 'A');

    SAVEPOINT after_first_insert;

    INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
    VALUES (9, 999, '2024-07-01', 'B');

ROLLBACK TO SAVEPOINT after_first_insert;

COMMIT;

SELECT * FROM enrollments WHERE student_id = 9;

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- END OF HANDS-ON 3
