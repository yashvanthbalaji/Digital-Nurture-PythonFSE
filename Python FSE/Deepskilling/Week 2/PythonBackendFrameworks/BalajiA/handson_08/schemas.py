from pydantic import BaseModel
from typing import Optional, List, Any


# ── COURSE SCHEMAS ──────────────────────────────────────────
class CourseCreate(BaseModel):
    # Used for POST and PUT — all fields required
    name: str
    code: str
    credits: int
    department_id: int

class CourseUpdate(BaseModel):
    # Used for PATCH — all fields optional
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None

class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int
    model_config = {"from_attributes": True}


# ── STUDENT SCHEMAS ─────────────────────────────────────────
class StudentCreate(BaseModel):
    # Used for POST and PUT — all fields required
    first_name: str
    last_name: str
    email: str
    enrollment_year: int

class StudentUpdate(BaseModel):
    # Used for PATCH — all fields optional
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    enrollment_year: Optional[int] = None

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    enrollment_year: int
    model_config = {"from_attributes": True}


# ── ENROLLMENT SCHEMAS ──────────────────────────────────────
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: str
    grade: Optional[str] = None

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrollment_date: str
    grade: Optional[str] = None
    model_config = {"from_attributes": True}


# ── PAGINATION ENVELOPE ─────────────────────────────────────
# This is the standard DRF-style pagination response shape
class PaginatedResponse(BaseModel):
    count: int                    # total number of items in DB
    next: Optional[str] = None    # URL of next page, null if last page
    previous: Optional[str] = None  # URL of previous page, null if first
    results: List[Any]            # the actual list of items