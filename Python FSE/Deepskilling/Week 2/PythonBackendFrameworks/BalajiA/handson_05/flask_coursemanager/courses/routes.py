from flask import Blueprint, jsonify, request
from extensions import db
from courses.models import Course, Student, Enrollment

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')


# Helper — always returns same JSON structure
def make_response_json(data, status_code=200):
    return jsonify({
        'status': 'success',
        'data': data
    }), status_code


# ── GET all courses from database ─────────────────────────────
@courses_bp.route('/', methods=['GET'])
def get_courses():
    # Course.query.all() fetches every row from the course table
    courses = Course.query.all()
    # to_dict() converts each Course object to a plain dict for JSON
    return make_response_json([c.to_dict() for c in courses])


# ── POST create new course in database ───────────────────────
@courses_bp.route('/', methods=['POST'])
def create_course():
    data = request.get_json()

    if data is None:
        return jsonify({'status': 'error', 'message': 'Send JSON with Content-Type: application/json'}), 400

    required_fields = ['name', 'code', 'credits', 'department_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'status': 'error', 'message': f'Missing field: {field}'}), 400

    # Create Course object and save to database
    course = Course(
        name=data['name'],
        code=data['code'],
        credits=data['credits'],
        department_id=data['department_id']
    )
    db.session.add(course)    # stage the object
    db.session.commit()       # actually save to DB

    return make_response_json(course.to_dict(), 201)


# ── GET one course by id ──────────────────────────────────────
@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    # get_or_404 = find by id, or automatically return 404 if not found
    course = Course.query.get_or_404(course_id)
    return make_response_json(course.to_dict())


# ── PUT update a course ───────────────────────────────────────
@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)

    data = request.get_json()
    if data is None:
        return jsonify({'status': 'error', 'message': 'Send JSON'}), 400

    # Update only fields that were actually sent
    if 'name' in data:
        course.name = data['name']
    if 'code' in data:
        course.code = data['code']
    if 'credits' in data:
        course.credits = data['credits']
    if 'department_id' in data:
        course.department_id = data['department_id']

    db.session.commit()   # save changes
    return make_response_json(course.to_dict())


# ── DELETE a course ───────────────────────────────────────────
@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return make_response_json({'message': f'Course {course_id} deleted'})


# ── GET students enrolled in a course (JOIN query) ────────────
@courses_bp.route('/<int:course_id>/students/', methods=['GET'])
def get_course_students(course_id):
    # First confirm the course exists
    course = Course.query.get_or_404(course_id)
    # Find all enrollment records for this course
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    # Get the student from each enrollment using the relationship
    students = [e.student.to_dict() for e in enrollments]
    return make_response_json(students)