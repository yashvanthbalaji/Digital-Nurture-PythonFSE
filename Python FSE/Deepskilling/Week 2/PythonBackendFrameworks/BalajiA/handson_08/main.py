from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete as sql_delete, func, or_
from typing import Optional, List
from contextlib import asynccontextmanager

import models
import schemas
from database import engine, get_db, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


# ── VERSIONING STRATEGY COMMENT (Task 2 Step 82) ────────────
# We use URL versioning: /api/v1/courses/
#
# Strategy 1 — URL Versioning (what we use here):
#   /api/v1/courses/  →  /api/v2/courses/
#   Pros: visible in browser, easy to test, easy to document
#   Cons: URLs get longer, must maintain multiple URL trees
#
# Strategy 2 — Header Versioning:
#   Client sends header: Accept: application/vnd.api+json;version=1
#   Pros: clean URLs, no URL changes between versions
#   Cons: hard to test in browser, harder to document


app = FastAPI(
    title='Course Management API',
    description='''
A RESTful API following industry best practices.

**Version:** v1 | **Base URL:** /api/v1/

**What changed from v0 to v1:**
- All URLs versioned: /api/v1/
- PATCH added alongside PUT (partial vs full update)
- POST returns Location header
- Pagination envelope: count, next, previous, results
- Search filter on GET /api/v1/courses/
- Standardised error format for all errors
    ''',
    version='1.0',
    contact={'name': 'Balaji A', 'email': 'balaji@college.edu'},
    lifespan=lifespan
)


# ── STANDARD ERROR FORMAT (Task 2 Step 85) ──────────────────
# Every error in this API follows this exact JSON shape:
# {"error": {"code": "NOT_FOUND", "message": "...", "field": null}}
def make_error(code: str, message: str, field: str = None):
    return {"error": {"code": code, "message": message, "field": field}}


# Override FastAPI's default HTTPException response format
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    code_map = {
        400: 'BAD_REQUEST',
        401: 'UNAUTHORIZED',
        403: 'FORBIDDEN',
        404: 'NOT_FOUND',
        422: 'VALIDATION_ERROR',
        500: 'INTERNAL_ERROR'
    }
    error_code = code_map.get(exc.status_code, 'ERROR')
    return JSONResponse(
        status_code=exc.status_code,
        content=make_error(error_code, str(exc.detail))
    )


# Override FastAPI's default 422 validation error format
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    field = str(errors[0]['loc'][-1]) if errors else None
    message = errors[0]['msg'] if errors else 'Validation error'
    return JSONResponse(
        status_code=422,
        content=make_error('VALIDATION_ERROR', message, field)
    )


# Background task for enrollment confirmation
def send_confirmation_email(student_email: str):
    print(f'[Background Task] Sending confirmation to: {student_email}')


# Root
@app.get('/', tags=['Root'])
async def root():
    return {'message': 'Course Management API v1', 'docs': '/docs', 'version': 'v1'}


# ════════════════════════════════════════════════════════
#  COURSES — /api/v1/courses/  (versioned URL)
# ════════════════════════════════════════════════════════

@app.post(
    '/api/v1/courses/',
    response_model=schemas.CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Courses'],
    summary='Create course — returns 201 + Location header'
)
async def create_course(
    course: schemas.CourseCreate,
    response: Response,            # inject Response to set headers
    db: AsyncSession = Depends(get_db)
):
    new_course = models.Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    # Location header tells the client WHERE to find the new resource
    response.headers['Location'] = f'/api/v1/courses/{new_course.id}'
    return new_course


@app.get(
    '/api/v1/courses/',
    tags=['Courses'],
    summary='Get courses — pagination (page/page_size) + search + filter'
)
async def get_courses(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    # Start with base queries
    base_query = select(models.Course)
    count_query = select(func.count(models.Course.id))

    # Case-insensitive search on name AND code (Task 2 Step 84)
    if search:
        search_filter = or_(
            models.Course.name.ilike(f'%{search}%'),
            models.Course.code.ilike(f'%{search}%')
        )
        base_query = base_query.where(search_filter)
        count_query = count_query.where(search_filter)

    # Optional department filter
    if department_id is not None:
        dept_filter = models.Course.department_id == department_id
        base_query = base_query.where(dept_filter)
        count_query = count_query.where(dept_filter)

    # Get total count BEFORE pagination
    total = (await db.execute(count_query)).scalar()

    # Apply pagination
    skip = (page - 1) * page_size
    result = await db.execute(base_query.offset(skip).limit(page_size))
    courses = result.scalars().all()

    # Build next/previous URLs
    base_url = f'/api/v1/courses/?page_size={page_size}'
    next_url = f'{base_url}&page={page+1}' if (skip + page_size) < total else None
    prev_url = f'{base_url}&page={page-1}' if page > 1 else None

    # Return pagination envelope (Task 2 Step 83)
    return {
        'count': total,
        'next': next_url,
        'previous': prev_url,
        'results': [schemas.CourseResponse.model_validate(c) for c in courses]
    }


@app.get('/api/v1/courses/{course_id}', response_model=schemas.CourseResponse, tags=['Courses'], summary='Get one course by ID')
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course).where(models.Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail=f'Course with id {course_id} does not exist')
    return course


@app.put(
    '/api/v1/courses/{course_id}',
    response_model=schemas.CourseResponse,
    tags=['Courses'],
    summary='FULL update — ALL fields required'
)
async def update_course(
    course_id: int,
    course_data: schemas.CourseCreate,   # All fields required = correct for PUT
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.Course).where(models.Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail=f'Course with id {course_id} does not exist')
    for key, value in course_data.model_dump().items():
        setattr(course, key, value)
    await db.commit()
    await db.refresh(course)
    return course


@app.patch(
    '/api/v1/courses/{course_id}',
    response_model=schemas.CourseResponse,
    tags=['Courses'],
    summary='PARTIAL update — send only the fields you want'
)
async def patch_course(
    course_id: int,
    course_data: schemas.CourseUpdate,   # All fields optional = correct for PATCH
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.Course).where(models.Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail=f'Course with id {course_id} does not exist')
    # exclude_unset=True means only update what was actually sent
    for key, value in course_data.model_dump(exclude_unset=True).items():
        setattr(course, key, value)
    await db.commit()
    await db.refresh(course)
    return course


@app.delete('/api/v1/courses/{course_id}', status_code=204, tags=['Courses'], summary='Delete course — returns 204 no body')
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course).where(models.Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail=f'Course with id {course_id} does not exist')
    await db.execute(sql_delete(models.Enrollment).where(models.Enrollment.course_id == course_id))
    await db.delete(course)
    await db.commit()
    return None


@app.get('/api/v1/courses/{course_id}/students/', response_model=List[schemas.StudentResponse], tags=['Courses'], summary='Students enrolled in a course')
async def get_course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course).where(models.Course.id == course_id))
    if result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail=f'Course with id {course_id} does not exist')
    enroll_result = await db.execute(select(models.Enrollment).where(models.Enrollment.course_id == course_id))
    students = []
    for e in enroll_result.scalars().all():
        s_res = await db.execute(select(models.Student).where(models.Student.id == e.student_id))
        s = s_res.scalar_one_or_none()
        if s:
            students.append(s)
    return students


# ════════════════════════════════════════════════════════
#  STUDENTS — /api/v1/students/
# ════════════════════════════════════════════════════════

@app.post('/api/v1/students/', response_model=schemas.StudentResponse, status_code=201, tags=['Students'], summary='Create student')
async def create_student(student: schemas.StudentCreate, response: Response, db: AsyncSession = Depends(get_db)):
    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    response.headers['Location'] = f'/api/v1/students/{new_student.id}'
    return new_student


@app.get('/api/v1/students/', response_model=List[schemas.StudentResponse], tags=['Students'], summary='Get all students')
async def get_students(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).offset(skip).limit(limit))
    return result.scalars().all()


@app.get('/api/v1/students/{student_id}', response_model=schemas.StudentResponse, tags=['Students'], summary='Get student by ID')
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).where(models.Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail=f'Student with id {student_id} does not exist')
    return student


@app.put('/api/v1/students/{student_id}', response_model=schemas.StudentResponse, tags=['Students'], summary='PUT = full update student')
async def update_student(student_id: int, student_data: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).where(models.Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail=f'Student with id {student_id} does not exist')
    for key, value in student_data.model_dump().items():
        setattr(student, key, value)
    await db.commit()
    await db.refresh(student)
    return student


@app.patch('/api/v1/students/{student_id}', response_model=schemas.StudentResponse, tags=['Students'], summary='PATCH = partial update student')
async def patch_student(student_id: int, student_data: schemas.StudentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).where(models.Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail=f'Student with id {student_id} does not exist')
    for key, value in student_data.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    await db.commit()
    await db.refresh(student)
    return student


@app.delete('/api/v1/students/{student_id}', status_code=204, tags=['Students'], summary='Delete student')
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).where(models.Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail=f'Student with id {student_id} does not exist')
    await db.execute(sql_delete(models.Enrollment).where(models.Enrollment.student_id == student_id))
    await db.delete(student)
    await db.commit()
    return None


# ════════════════════════════════════════════════════════
#  ENROLLMENTS — /api/v1/enrollments/
# ════════════════════════════════════════════════════════

@app.post('/api/v1/enrollments/', response_model=schemas.EnrollmentResponse, status_code=201, tags=['Enrollments'], summary='Enroll student in course')
async def create_enrollment(
    enrollment: schemas.EnrollmentCreate,
    response: Response,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    new_enrollment = models.Enrollment(**enrollment.model_dump())
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)
    response.headers['Location'] = f'/api/v1/enrollments/{new_enrollment.id}'
    s_result = await db.execute(select(models.Student).where(models.Student.id == enrollment.student_id))
    student = s_result.scalar_one_or_none()
    if student:
        background_tasks.add_task(send_confirmation_email, student.email)
    return new_enrollment


@app.get('/api/v1/enrollments/', response_model=List[schemas.EnrollmentResponse], tags=['Enrollments'], summary='Get all enrollments')
async def get_enrollments(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment).offset(skip).limit(limit))
    return result.scalars().all()


@app.delete('/api/v1/enrollments/{enrollment_id}', status_code=204, tags=['Enrollments'], summary='Delete enrollment')
async def delete_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment).where(models.Enrollment.id == enrollment_id))
    enrollment = result.scalar_one_or_none()
    if enrollment is None:
        raise HTTPException(status_code=404, detail=f'Enrollment with id {enrollment_id} does not exist')
    await db.delete(enrollment)
    await db.commit()
    return None