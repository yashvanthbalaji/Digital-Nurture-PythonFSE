# Digital Nurture 5.0 | Module 3: Database Integration
# Hands-On 6 & 7 - SQLAlchemy Models
# Name   : Balaji A


from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, CHAR, Boolean, Time, create_engine
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Department(Base):
    __tablename__ = 'departments'

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name     = Column(String(100), nullable=False)
    head_of_dept  = Column(String(100))
    budget        = Column(Numeric(12, 2))

    students   = relationship('Student',   back_populates='department')
    professors = relationship('Professor', back_populates='department')
    courses    = relationship('Course',    back_populates='department')


class Student(Base):
    __tablename__ = 'students'

    student_id      = Column(Integer, primary_key=True, autoincrement=True)
    first_name      = Column(String(50),  nullable=False)
    last_name       = Column(String(50),  nullable=False)
    email           = Column(String(100), unique=True, nullable=False)
    date_of_birth   = Column(Date)
    department_id   = Column(Integer, ForeignKey('departments.department_id'))
    enrollment_year = Column(Integer)
    is_active       = Column(Boolean, default=True)   # Step 98: added in HO7 Task 2

    department  = relationship('Department', back_populates='students')
    enrollments = relationship('Enrollment', back_populates='student')


class Course(Base):
    __tablename__ = 'courses'

    course_id     = Column(Integer, primary_key=True, autoincrement=True)
    course_name   = Column(String(150), nullable=False)
    course_code   = Column(String(20),  unique=True)
    credits       = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.department_id'))

    department  = relationship('Department', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course')
    schedules   = relationship('CourseSchedule', back_populates='course')


class Enrollment(Base):
    __tablename__ = 'enrollments'

    enrollment_id   = Column(Integer, primary_key=True, autoincrement=True)
    student_id      = Column(Integer, ForeignKey('students.student_id'))
    course_id       = Column(Integer, ForeignKey('courses.course_id'))
    enrollment_date = Column(Date)
    grade           = Column(CHAR(2))

    student = relationship('Student', back_populates='enrollments')
    course  = relationship('Course',  back_populates='enrollments')


class Professor(Base):
    __tablename__ = 'professors'

    professor_id  = Column(Integer, primary_key=True, autoincrement=True)
    prof_name     = Column(String(100), nullable=False)
    email         = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    salary        = Column(Numeric(10, 2))

    department = relationship('Department', back_populates='professors')


# Step 102: New table added in HO7 Task 2
class CourseSchedule(Base):
    __tablename__ = 'course_schedules'

    schedule_id  = Column(Integer, primary_key=True, autoincrement=True)
    course_id    = Column(Integer, ForeignKey('courses.course_id'))
    day_of_week  = Column(String(10), nullable=False)
    start_time   = Column(Time, nullable=False)
    end_time     = Column(Time, nullable=False)

    course = relationship('Course', back_populates='schedules')


# Engine
engine = create_engine(
    'mysql+mysqlconnector://root:yashvanth%4016@localhost/college_db_orm',
    echo=True
)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print("====================================")
    print("All tables created in college_db_orm!")
    print("====================================")