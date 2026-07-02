from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete as sql_delete
from typing import Optional, List
from contextlib import asynccontextmanager

import models
import schemas
from database import engine, get_db, Base


# Creates all tables in DB when server starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


#  TASK 2: OpenAPI Customisation
app = FastAPI(
    title='Course Management API',
    description='''
A complete REST API for managing college courses, students and enrollments.

**Features:**
- Full CRUD for Courses, Students and Enrollments
- Pagination and filtering support
- Background email confirmation on enrollment
    ''',
    version='1.0',
    contact={
        'name': 'Balaji A',
        'email': 'balaji@college.edu'
    },
    lifespan=lifespan
)


#  BACKGROUND TASK FUNCTION
# This function runs AFTER the response is already sent to user
# Useful for emails, logging, — non-urgent tasks
def send_confirmation_email(student_email: str):
    print(f'[Background Task] Sending confirmation email to: {student_email}')


# ── ROOT ─────────────────────────────────────────────────────
@app.get('/', tags=['Root'])
async def root():
    return {'message': 'Course Management API is running'}


#  COURSE ENDPOINTS — tags=['Courses'] groups them in /docs

@app.post(
    '/api/courses/',
    response_model=schemas.CourseResponse,
    status_code=status.HTTP_201_CREATED,   # 201 = Created
    tags=['Courses'],
    summary='Create a new course',
    response_description='The newly created course object'
)
async def create_course(
    course: schemas.CourseCreate,
    db: AsyncSession = Depends(get_db)
):
    new_course = models.Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@app.get(
    '/api/courses/',
    response_model=List[schemas.CourseResponse],
    tags=['Courses'],
    summary='Get all courses with pagination and filtering'
)
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Course)
    if department_id is not None:
        query = query.where(models.Course.department_id == department_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@app.get(
    '/api/courses/{course_id}',
    response_model=schemas.CourseResponse,
    tags=['Courses'],
    summary='Get a single course by ID'
)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Course).where(models.Course.id == course_id)
    )
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


@app.put(
    '/api/courses/{course_id}',
    response_model=schemas.CourseResponse,
    tags=['Courses'],
    summary='Update a course — send only the fields you want to change'
)
async def update_course(
    course_id: int,
    course_data: schemas.CourseUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.Course).where(models.Course.id == course_id)
    )
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    # Only update fields that were actually sent
    for key, value in course_data.model_dump(exclude_unset=True).items():
        setattr(course, key, value)
    await db.commit()
    await db.refresh(course)
    return course


@app.delete(
    '/api/courses/{course_id}',
    status_code=status.HTTP_204_NO_CONTENT,   # 204 = Deleted, no body
    tags=['Courses'],
    summary='Delete a course'
)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Course).where(models.Course.id == course_id)
    )
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')

    # If we delete the course directly, DB blocks it because of active enrollments
    enroll_result = await db.execute(
        select(models.Enrollment).where(models.Enrollment.course_id == course_id)
    )
    for enrollment in enroll_result.scalars().all():
        await db.delete(enrollment)

    await db.delete(course)
    await db.commit()
    return None   # 204 means return nothing


@app.get(
    '/api/courses/{course_id}/students/',
    response_model=List[schemas.StudentResponse],
    tags=['Courses'],
    summary='Get all students enrolled in a specific course'
)
async def get_course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Course).where(models.Course.id == course_id)
    )
    if result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail='Course not found')
    # Find all enrollments for this course then get each student
    enroll_result = await db.execute(
        select(models.Enrollment).where(models.Enrollment.course_id == course_id)
    )
    enrollments = enroll_result.scalars().all()
    students = []
    for e in enrollments:
        s_result = await db.execute(
            select(models.Student).where(models.Student.id == e.student_id)
        )
        student = s_result.scalar_one_or_none()
        if student:
            students.append(student)
    return students


#  STUDENT ENDPOINTS

@app.post(
    '/api/students/',
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Students'],
    summary='Create a new student'
)
async def create_student(student: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student


@app.get(
    '/api/students/',
    response_model=List[schemas.StudentResponse],
    tags=['Students'],
    summary='Get all students'
)
async def get_students(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).offset(skip).limit(limit))
    return result.scalars().all()


@app.get(
    '/api/students/{student_id}',
    response_model=schemas.StudentResponse,
    tags=['Students'],
    summary='Get a student by ID'
)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Student).where(models.Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    return student


@app.put(
    '/api/students/{student_id}',
    response_model=schemas.StudentResponse,
    tags=['Students'],
    summary='Update a student'
)
async def update_student(
    student_id: int,
    student_data: schemas.StudentUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.Student).where(models.Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    for key, value in student_data.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    await db.commit()
    await db.refresh(student)
    return student


#  ENROLLMENT ENDPOINTS — Background task is here!

@app.post(
    '/api/enrollments/',
    response_model=schemas.EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Enrollments'],
    summary='Enroll a student in a course — sends email confirmation in background'
)
async def create_enrollment(
    enrollment: schemas.EnrollmentCreate,
    background_tasks: BackgroundTasks,       # FastAPI injects this automatically
    db: AsyncSession = Depends(get_db)
):
    new_enrollment = models.Enrollment(**enrollment.model_dump())
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)

    # Get student to find their email
    s_result = await db.execute(
        select(models.Student).where(models.Student.id == enrollment.student_id)
    )
    student = s_result.scalar_one_or_none()
    if student:
        # This task runs AFTER 201 response is already sent to user
        background_tasks.add_task(send_confirmation_email, student.email)

    return new_enrollment


@app.get(
    '/api/enrollments/',
    response_model=List[schemas.EnrollmentResponse],
    tags=['Enrollments'],
    summary='Get all enrollments'
)
async def get_enrollments(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment).offset(skip).limit(limit))
    return result.scalars().all()


@app.delete(
    '/api/enrollments/{enrollment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Enrollments'],
    summary='Delete an enrollment'
)
async def delete_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Enrollment).where(models.Enrollment.id == enrollment_id)
    )
    enrollment = result.scalar_one_or_none()
    if enrollment is None:
        raise HTTPException(status_code=404, detail='Enrollment not found')
    await db.delete(enrollment)
    await db.commit()
    return None