from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from contextlib import asynccontextmanager

import models
import schemas
from database import engine, get_db, Base


# lifespan = code that runs when server STARTS and STOPS
# Here we create all DB tables automatically on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield   # server runs here
    # cleanup code after yield runs when server stops


# Create the FastAPI app
# title and version appear in the auto-generated /docs page
app = FastAPI(
    title='Course Management API',
    version='1.0',
    lifespan=lifespan
)


# ── ROOT ROUTE ───────────────────────────────────────────────
@app.get('/')
async def root():
    return {'message': 'Course Management API is running'}


# ── POST: Create a new course ────────────────────────────────
# CourseCreate = what user must send
# CourseResponse = what we return back
# status_code=201 = "created successfully"
@app.post('/api/courses/', response_model=schemas.CourseResponse, status_code=201)
async def create_course(
    course: schemas.CourseCreate,
    db: AsyncSession = Depends(get_db)   # inject DB session
):
    # course.model_dump() converts Pydantic model to a dict
    new_course = models.Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)   # reload from DB to get the new id
    return new_course


# ── GET: All courses with pagination and filtering ───────────
# skip and limit = pagination (like pages)
# department_id = optional filter
@app.get('/api/courses/', response_model=List[schemas.CourseResponse])
async def get_courses(
    skip: int = 0,                         # how many to skip (default 0)
    limit: int = 10,                       # how many to return (default 10)
    department_id: Optional[int] = None,   # filter by department
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Course)

    # Apply filter only if department_id was provided in URL
    if department_id is not None:
        query = query.where(models.Course.department_id == department_id)

    # Apply pagination
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    courses = result.scalars().all()
    return courses


# ── GET: One course by id ────────────────────────────────────
# {course_id} in URL is a path parameter — FastAPI auto-validates it as int
@app.get('/api/courses/{course_id}', response_model=schemas.CourseResponse)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.Course).where(models.Course.id == course_id)
    )
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


# ── PUT: Update a course ─────────────────────────────────────
@app.put('/api/courses/{course_id}', response_model=schemas.CourseResponse)
async def update_course(
    course_id: int,
    course_data: schemas.CourseUpdate,   # all fields optional
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.Course).where(models.Course.id == course_id)
    )
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')

    # exclude_unset=True means only update fields that were actually sent
    update_data = course_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)

    await db.commit()
    await db.refresh(course)
    return course


# ── DELETE: Remove a course ──────────────────────────────────
@app.delete('/api/courses/{course_id}')
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.Course).where(models.Course.id == course_id)
    )
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')

    await db.delete(course)
    await db.commit()
    return {'message': f'Course {course_id} deleted successfully'}