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
    
-- 26. Show each enrollment along with the student's name and the course name. (3-table JOIN:
-- enrollments, students, courses.)

-- DIUBTTTTTTTTTTTTTTT
describe courses;

SELECT CONCAT(first_name , ' ' , last_name ) AS Student_name , course_name , enrollment_id
FROM enrollment e INNER JOIN students s ON e.enrollment_id = s.student_id
INNER JOIN courses c ON c.course_id = 
    
  -- -------------------------------------------------------
  
-- 27. Find all students who are NOT enrolled in any course using a LEFT JOIN and WHERE ... IS NULL
-- pattern

SELECT CONCAT(s.first_name ,' ' ,s.last_name ) AS studentname, e.enrollment_id
FROM students s LEFT JOIN enrollments e 
ON s.student_id = e.student_id
WHERE e.enrollment_id is NULL;

-- 28. Display every course along with the number of students enrolled in it. Courses with zero enrolments
-- must still appear. (LEFT JOIN courses with enrollments, GROUP BY course.)
  
SELECT c.course_name , c.course_code, count(e.enrollment_id)
from courses c LEFT JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_name, c.course_code;

-- 29. List each department along with its professors and their salaries. Include departments that have no
-- professors yet.

SELECT d.dept_name , p.prof_name , p.salary
FROM departments d LEFT JOIN professors p
ON d.department_id = p.department_id;
ORDER  BY d.dept_name;

-- TASK 4: Aggregations and Grouping

-- 30. Calculate the total number of enrollments per course. Display course_name and enrollment_count.




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    