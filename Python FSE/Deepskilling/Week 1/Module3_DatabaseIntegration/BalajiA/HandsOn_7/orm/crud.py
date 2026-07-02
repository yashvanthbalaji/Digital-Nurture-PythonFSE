# Digital Nurture 5.0 | Module 3: Database Integration
# Hands-On 6 - Task 2 & 3: CRUD Operations + Eager Loading
# Name   : BALAJI A


# Step 90: N+1 Comparison - document at top of file as instructed
# WITHOUT joinedload (Step 84 - Lazy Loading):
#   Query 1 : SELECT * FROM enrollments         → fetches all enrollments
#   Query 2 : SELECT * FROM students WHERE id=1 → for enrollment 1
#   Query 3 : SELECT * FROM courses  WHERE id=1 → for enrollment 1
#   Query 4 : SELECT * FROM students WHERE id=2 → for enrollment 2
#   ... and so on for every enrollment row
#   Total queries = 1 + (N x 2) → N+1 problem!
#
# WITH joinedload (Step 88 - Eager Loading):
#   Query 1 : SELECT enrollments JOIN students JOIN courses → all in ONE query
#   Total queries = 1
#
# Conclusion: joinedload reduced queries from many → 1 (eliminated N+1)

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, Department, Student, Course, Enrollment, Professor

# Step 80: Create engine with echo=True and open Session
engine = create_engine(
    'mysql+mysqlconnector://root:yashvanth%4016@localhost/college_db_orm',
    echo=True
)

Session = sessionmaker(bind=engine)
session = Session()

print("\n====================================")
print("TASK 2: CRUD Operations via ORM")
print("====================================")

# Step 81: INSERT 3 Department objects and 5 Student objects

dept1 = Department(dept_name='Computer Science', head_of_dept='Dr. Ramesh Kumar', budget=850000.00)
dept2 = Department(dept_name='Electronics',      head_of_dept='Dr. Priya Nair',   budget=620000.00)
dept3 = Department(dept_name='Mechanical',       head_of_dept='Dr. Suresh Iyer',  budget=540000.00)

session.add_all([dept1, dept2, dept3])
session.commit()
print("\n-- 3 Departments inserted --")

s1 = Student(first_name='Arjun',  last_name='Mehta',  email='arjun.mehta@college.edu',  department_id=1, enrollment_year=2022)
s2 = Student(first_name='Priya',  last_name='Suresh', email='priya.suresh@college.edu', department_id=1, enrollment_year=2022)
s3 = Student(first_name='Rohan',  last_name='Verma',  email='rohan.verma@college.edu',  department_id=2, enrollment_year=2021)
s4 = Student(first_name='Sneha',  last_name='Patel',  email='sneha.patel@college.edu',  department_id=3, enrollment_year=2023)
s5 = Student(first_name='Vikram', last_name='Das',    email='vikram.das@college.edu',   department_id=1, enrollment_year=2022)

session.add_all([s1, s2, s3, s4, s5])
session.commit()
print("\n-- 5 Students inserted --")

# Step 82: INSERT 3 Course objects and 4 Enrollment objects

c1 = Course(course_name='Data Structures & Algorithms', course_code='CS101', credits=4, department_id=1)
c2 = Course(course_name='Database Management Systems',  course_code='CS102', credits=3, department_id=1)
c3 = Course(course_name='Object Oriented Programming',  course_code='CS103', credits=4, department_id=1)

session.add_all([c1, c2, c3])
session.commit()
print("\n-- 3 Courses inserted --")

e1 = Enrollment(student_id=1, course_id=1, enrollment_date=date(2022, 7, 1), grade='A')
e2 = Enrollment(student_id=1, course_id=2, enrollment_date=date(2022, 7, 1), grade='B')
e3 = Enrollment(student_id=2, course_id=1, enrollment_date=date(2022, 7, 1), grade='B')
e4 = Enrollment(student_id=2, course_id=3, enrollment_date=date(2022, 7, 1), grade='A')

session.add_all([e1, e2, e3, e4])
session.commit()
print("\n-- 4 Enrollments inserted --")

# Step 83: READ - students in Computer Science department

print("\n-- Students in Computer Science --")
cs_students = session.query(Student).join(Department).filter(
    Department.dept_name == 'Computer Science'
).all()

for s in cs_students:
    print(f"  {s.first_name} {s.last_name}")

# Step 84: READ - all enrollments with student name + course name
# echo=True on engine prints every SQL query issued
# Count the SQL lines printed to detect N+1

print("\n-- All Enrollments with Student and Course (Lazy Load) --")
enrollments = session.query(Enrollment).all()

for e in enrollments:
    print(f"  {e.student.first_name} {e.student.last_name} → {e.course.course_name} | Grade: {e.grade}")


# Step 85: UPDATE - find student by email and update enrollment_year

print("\n-- UPDATE: Changing enrollment_year for arjun.mehta --")
student_to_update = session.query(Student).filter(
    Student.email == 'arjun.mehta@college.edu'
).first()

student_to_update.enrollment_year = 2023
session.commit()
print(f"  Updated: {student_to_update.first_name} enrollment_year → {student_to_update.enrollment_year}")

# Step 86: DELETE - remove one enrollment record

print("\n-- DELETE: Removing enrollment_id = 4 --")
enrollment_to_delete = session.query(Enrollment).filter(
    Enrollment.enrollment_id == 4
).first()

session.delete(enrollment_to_delete)
session.commit()

remaining = session.query(Enrollment).count()
print(f"  Enrollment deleted. Remaining enrollments: {remaining}")

print("\n====================================")
print("TASK 3: Eager Loading to Fix N+1")
print("====================================")

# Step 87: N+1 identified in Step 84 above (check echo=True logs)
# Step 88: Fix using joinedload - loads everything in 1 SQL query


print("\n-- All Enrollments with joinedload (Eager Loading) --")
enrollments_eager = session.query(Enrollment).options(
    joinedload(Enrollment.student),
    joinedload(Enrollment.course)
).all()

for e in enrollments_eager:
    print(f"  {e.student.first_name} {e.student.last_name} → {e.course.course_name} | Grade: {e.grade}")

# Step 89: Count SQL queries in echo=True logs above
# With joinedload → only 1 SQL query issued (check terminal output)

# Step 91: Bonus - Django ORM equivalent (reference only)
# Enrollment.objects.select_related('student', 'course').all()
# select_related does the same as joinedload - single JOIN query

session.close()
print("\n-- Session closed --")