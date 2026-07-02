-- Digital Nurture 5.0 | Module 3: Database Integration
-- Hands-On 2: DML, Joins & Aggregations
-- Name: BALAJI A

-- use our database
USE college_db;
describe students;

-- TASK 1: Insert, Update and Delete Data


-- Step 16: Insert 2 additional students
INSERT INTO students(first_name, last_name, email, date_of_birth, department_id, enrollment_year)
VALUES ('Rahul',  'Sharma', 'rahul.sharma@college.edu',  '2003-06-15', 2, 2022),
('Nithya', 'Kumar',  'nithya.kumar@college.edu',  '2004-02-10', 3, 2023);

-- verify students table
SELECT * FROM students;

-- Step 17: Update grade of student_id=5, course_id=1 from C → B
-- checking
SELECT * FROM enrollments
WHERE student_id = 5 AND course_id = 1;

-- update grade
UPDATE enrollments 
SET grade ='B' WHERE student_id =5 AND course_id =1;

-- verify
SELECT * FROM enrollments
WHERE student_id = 5 AND course_id = 1;

-- Step 18: Delete enrollments where grade IS NULL
-- checking
SELECT * FROM enrollments
WHERE grade is null;

-- for deleting rows
SET SQL_SAFE_UPDATES =0;

-- delete row
DELETE FROM enrollments
WHERE grade IS NULL;

-- verify using count
SELECT COUNT(*) AS Total_Rows FROM enrollments;
SELECT * FROM enrollments
WHERE grade is null;   
    
-- TASK 2: Single-Table Queries and Filtering

-- 20. Retrieve all students enrolled in 2022, ordered by last_name alphabetically.

-- Preview
select * from students;

-- Retrieved
SELECT  student_id, first_name , last_name
FROM students
WHERE enrollment_year = 2022
ORDER BY last_name ASC;

-- 21. Find all courses with more than 3 credits, sorted by credits descending.

SELECT course_id , course_name , credits
FROM courses 
WHERE credits > 3
ORDER BY credits DESC;
    
-- 22. List all professors whose salary is between 80,000 and 95,000.

SELECT prof_name , salary
FROM professors
WHERE salary BETWEEN 80000 AND 95000;
    
-- 23. Find all students whose email ends with '@college.edu' using the LIKE operator.

SELECT first_name , last_name ,email
FROM students
WHERE email LIKE '%@college.edu';

-- 24. Count the total number of students per enrollment_year.

SELECT COUNT(student_id)  AS Total_number, enrollment_year
FROM students
GROUP BY enrollment_year
ORDER BY enrollment_year ASC;
    
-- TASK 3: Multi-Table Joins

-- 25. List each student's full name (first_name + ' ' + last_name) alongside the name of their department.
-- (JOIN students and departments.)

SELECT CONCAT(first_name , ' ' , last_name) AS Full_name, dept_name
FROM students INNER JOIN departments
ON students.department_id = departments.department_id;
    
-- Step 26: Enrollment + student name + course name (3-table JOIN)
SELECT CONCAT(s.first_name, ' ', s.last_name) AS student_name,
       c.course_name,
       e.enrollment_date,
       e.grade
FROM   enrollments e
INNER  JOIN students s ON e.student_id = s.student_id
INNER  JOIN courses  c ON e.course_id  = c.course_id;

    
 -- Step 27: Students NOT enrolled in any course
-- LEFT JOIN + IS NULL trick to find missing relationships
SELECT CONCAT(s.first_name, ' ', s.last_name) AS student_name,
       e.enrollment_id
FROM   students   s
LEFT   JOIN enrollments e ON s.student_id = e.student_id
WHERE  e.enrollment_id IS NULL;

-- Step 28: Every course + number of students enrolled
-- Courses with 0 enrollments must still appear → LEFT JOIN!
SELECT c.course_name,
       c.course_code,
       COUNT(e.enrollment_id) AS enrolled_students
FROM   courses    c
LEFT   JOIN enrollments e ON c.course_id = e.course_id
GROUP  BY c.course_id, c.course_name, c.course_code
ORDER  BY enrolled_students DESC;

-- Step 29: Every department + professors + salaries
-- Include departments with NO professors → LEFT JOIN!
SELECT d.dept_name,
       p.prof_name,
       p.salary
FROM   departments d
LEFT   JOIN professors p ON d.department_id = p.department_id
ORDER  BY d.dept_name;

-- TASK 4: Aggregations and Grouping


-- Step 30: Total enrollments per course
SELECT c.course_name,
       COUNT(e.enrollment_id) AS enrollment_count
FROM   courses     c
LEFT   JOIN enrollments e ON c.course_id = e.course_id
GROUP  BY c.course_id, c.course_name
ORDER  BY enrollment_count DESC;

-- Step 31: Average professor salary per department (rounded to 2 decimals)
-- Expected: 4 rows, one per department
SELECT d.dept_name,
       ROUND(AVG(p.salary), 2) AS avg_salary
FROM   departments d
INNER  JOIN professors p ON d.department_id = p.department_id
GROUP  BY d.department_id, d.dept_name;

-- Step 32: Departments where total budget exceeds 600,000
SELECT dept_name, budget
FROM   departments
WHERE  budget > 600000;

-- Step 33: Grade distribution for course CS101
SELECT e.grade,
       COUNT(*) AS grade_count
FROM   enrollments e
INNER  JOIN courses c ON e.course_id = c.course_id
WHERE  c.course_code = 'CS101'
GROUP  BY e.grade
ORDER  BY e.grade;

-- Step 34: Departments where more than 2 students are enrolled
-- HAVING filters AFTER grouping (unlike WHERE which filters rows)
SELECT d.dept_name,
       COUNT(e.enrollment_id) AS total_enrollments
FROM   departments  d
INNER  JOIN students   s ON d.department_id = s.department_id
INNER  JOIN enrollments e ON s.student_id   = e.student_id
GROUP  BY d.department_id, d.dept_name
HAVING COUNT(e.enrollment_id) > 2
ORDER  BY total_enrollments DESC;

-- END OF HANDS-ON 2