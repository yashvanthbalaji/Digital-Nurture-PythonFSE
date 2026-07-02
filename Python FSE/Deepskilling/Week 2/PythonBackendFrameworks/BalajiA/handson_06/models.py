from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Department table
class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    head_of_dept = Column(String(100), nullable=False)
    budget = Column(Numeric(10, 2), nullable=False)

    # One department has many courses
    courses = relationship('Course', back_populates='department')


# Course table
class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)

    department = relationship('Department', back_populates='courses')