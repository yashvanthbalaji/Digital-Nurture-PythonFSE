from pydantic import BaseModel
from typing import Optional, List

# ── COURSE SCHEMAS ──────────────────────────────────────────

# Used for POST — creating a new course
# All fields are REQUIRED when creating
class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int

# Used for PUT — updating a course
# All fields are OPTIONAL — send only what you want to change
class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None

# Used for GET response — what we RETURN to the user
# Includes id (which we never ask the user to send)
class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int

    # This tells Pydantic: also accept SQLAlchemy ORM objects
    # not just plain dicts
    model_config = {"from_attributes": True}


# ── DEPARTMENT SCHEMA ────────────────────────────────────────

# Demonstrates nested Pydantic models
# DepartmentResponse contains a list of CourseResponse inside it
class DepartmentResponse(BaseModel):
    id: int
    name: str
    head_of_dept: str
    budget: float
    courses: List[CourseResponse] = []   # nested list of courses

    model_config = {"from_attributes": True}