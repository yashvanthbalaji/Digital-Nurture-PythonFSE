-- Digital Nurture 5.0 | Module 3: Database Integration
-- Hands-On 1: Schema Design & Core SQL
-- Name: Balaji A
-- ----------------------------------------------------------------------------------------------------------
-- TASK 1: Create Database and Tables

-- create databse
create database college_db;
use college_db;

-- Step 1: Create departments table
create table departments (
department_id INT PRIMARY KEY AUTO_INCREMENT,
dept_name VARCHAR(100) NOT NULL,
hod_name VARCHAR(100),
budget DECIMAL(12,2)
);

-- Step 2: Create students table
create table students(
student_id INT PRIMARY KEY AUTO_INCREMENT,
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
date_of_birth DATE,
department_id INT,
FOREIGN KEY ( department_id )
REFERENCES departments(department_id),
enrollment_year INT
);

-- Step 3: Create students table
create table courses(
course_id INT PRIMARY KEY AUTO_INCREMENT,
course_name VARCHAR(150) NOT NULL,
course_code VARCHAR(20) UNIQUE,
credits INT,
department_id INT,
FOREIGN KEY (department_id)
REFERENCES departments (department_id)
);

-- Step 4: Create enrollments table
create table enrollments(
enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
student_id INT,
course_id INT,
enrollment_date DATE,
grade CHAR(2),

FOREIGN KEY (student_id)
REFERENCES students (student_id),
FOREIGN KEY (course_id)
REFERENCES courses (course_id)
);

-- Step 5: Create professors table
create table professors(
professor_id INT PRIMARY KEY AUTO_INCREMENT,
prof_name VARCHAR(100) NOT NULL,
email VARCHAR(100) UNIQUE,
department_id INT,
salary DECIMAL(10,2),

FOREIGN KEY (department_id)
REFERENCES departments (department_id) 
);

-- Sample data for all tables

-- departments
INSERT INTO departments (dept_name, hod_name, budget) VALUES
 ('Computer Science', 'Dr. Ramesh Kumar', 850000.00),
 ('Electronics', 'Dr. Priya Nair', 620000.00),
 ('Mechanical', 'Dr. Suresh Iyer', 540000.00),
 ('Civil', 'Dr. Ananya Sharma', 430000.00);
-- students
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id,
enrollment_year) VALUES
 ('Arjun', 'Mehta', 'arjun.mehta@college.edu', '2003-04-12', 1, 2022),
 ('Priya', 'Suresh', 'priya.suresh@college.edu', '2003-07-25', 1, 2022),
 ('Rohan', 'Verma', 'rohan.verma@college.edu', '2002-11-08', 2, 2021),
 ('Sneha', 'Patel', 'sneha.patel@college.edu', '2004-01-30', 3, 2023),
 ('Vikram', 'Das', 'vikram.das@college.edu', '2003-09-14', 1, 2022),
 ('Kavya', 'Menon', 'kavya.menon@college.edu', '2002-05-17', 2, 2021),
 ('Aditya', 'Singh', 'aditya.singh@college.edu', '2004-03-22', 4, 2023),
 ('Deepika','Rao', 'deepika.rao@college.edu', '2003-08-09', 1, 2022);
-- courses
INSERT INTO courses (course_name, course_code, credits, department_id) VALUES
 ('Data Structures & Algorithms', 'CS101', 4, 1),
 ('Database Management Systems', 'CS102', 3, 1),
 ('Object Oriented Programming', 'CS103', 4, 1),
 ('Circuit Theory', 'EC101', 3, 2),
 ('Thermodynamics', 'ME101', 3, 3);
-- enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
 (1, 1, '2022-07-01', 'A'), (1, 2, '2022-07-01', 'B'),
 (2, 1, '2022-07-01', 'B'), (2, 3, '2022-07-01', 'A'),
 (3, 4, '2021-07-01', 'A'), (4, 5, '2023-07-01', NULL),
 (5, 1, '2022-07-01', 'C'), (5, 2, '2022-07-01', 'A'),
 (6, 4, '2021-07-01', 'B'), (7, 5, '2023-07-01', NULL),
 (8, 1, '2022-07-01', 'A'), (8, 3, '2022-07-01', 'B');
-- professors
INSERT INTO professors (prof_name, email, department_id, salary) VALUES
 ('Dr. Anand Krishnan', 'anand.k@college.edu', 1, 95000.00),
 ('Dr. Meena Pillai', 'meena.p@college.edu', 1, 88000.00),
 ('Dr. Sunil Rajan', 'sunil.r@college.edu', 2, 82000.00),
 ('Dr. Latha Gopal', 'latha.g@college.edu', 3, 79000.00),
 ('Dr. Kartik Bose', 'kartik.b@college.edu', 4, 76000.00);


-- TASK 2: Verify Normalisation

-- 1NF Analysis:
-- Rule: Every column must hold atomic (single) values.
-- Status: SATISFIED
-- All columns in college_db store one value per cell.
-- Hypothetical violation: storing '9876543210, 8123456789'
-- in one phone_number column would break 1NF.

-- 2NF Analysis:
-- Rule: Every non-key column must depend on the FULL primary key.
-- Table checked: enrollments (composite key: student_id + course_id)
-- Status: SATISFIED
-- 'grade' depends on BOTH student_id AND course_id together.
-- 'enrollment_date' also depends on both columns together.
-- Violation example: storing first_name in enrollments would be
-- a partial dependency (depends only on student_id) → breaks 2NF

-- 3NF Analysis:
-- Rule: No transitive dependencies allowed.
-- Status: SATISFIED
-- dept_name is NOT stored in the students table.
-- Only department_id (FK) is stored → dept_name fetched from departments.
-- If dept_name were in students:
-- student_id → department_id → dept_name (transitive) → breaks 3NF.
-- enrollments table: grade depends directly on (student_id + course_id).
-- No column depends on another non-key column. 3NF is fully satisfied.


-- Task 3: Alter and Extend the Schema

ALTER TABLE students 
ADD COLUMN phone_number VARCHAR(15);

ALTER TABLE courses
ADD COLUMN max_seats INT DEFAULT 60;

ALTER TABLE enrollments
ADD CONSTRAINT chk_grade CHECK(grade IN('A','B','C','D','F') OR grade IS NULL);

ALTER TABLE departments
CHANGE COLUMN hod_name head_of_dept VARCHAR(100);

ALTER TABLE students 
DROP COLUMN phone_number;

-- Verify using INFORMATION_SCHEMA

-- Confirm phone_number is GONE from students:
SELECT COLUMN_NAME, DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA ='college_db'
AND TABLE_NAME = 'students';

-- Confirm max_seats in courses:
SELECT COLUMN_NAME , DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'college_db'
AND TABLE_NAME ='courses'
AND COLUMN_NAME  = 'max_seats';

-- Confirm head_of_dept in departments
SELECT COLUMN_NAME , DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA ='college_db'
AND TABLE_NAME ='departments'
AND COLUMN_NAME ='head_of_dept';

-- Confirm chk_grade constraint on enrollments:
SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'college_db'
AND   TABLE_NAME   = 'enrollments'
AND   COLUMN_NAME  = 'grade';

SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'college_db'
AND   TABLE_NAME   = 'enrollments';

-- Completed Hand-On 1