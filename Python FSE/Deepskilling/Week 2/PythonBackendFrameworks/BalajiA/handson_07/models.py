from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    head_of_dept = Column(String(100), nullable=False)
    budget = Column(Numeric(10, 2), nullable=False)
    courses = relationship('Course', back_populates='department')


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    department = relationship('Department', back_populates='courses')
    # One course can have many enrollments
    enrollments = relationship('Enrollment', back_populates='course')


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    enrollment_year = Column(Integer, nullable=False)
    enrollments = relationship('Enrollment', back_populates='student')


class Enrollment(Base):
    __tablename__ = 'enrollment'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    enrollment_date = Column(String(20), nullable=False)
    grade = Column(String(2), nullable=True)
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')