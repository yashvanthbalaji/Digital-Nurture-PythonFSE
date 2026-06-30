from flask import Blueprint, jsonify, request

# Blueprint groups related routes together
# url_prefix means ALL routes here start with /api/courses
courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

# In-memory list to store courses (no database in this handson)
# NOTE: This resets every time the server restarts
courses_list = []
next_id = 1


# ── HELPER FUNCTION (Task 2) ─────────────────────────────────────
# Ensures all our success responses look exactly the same
def make_response_json(data, status_code=200):
    return jsonify({
        'status': 'success',
        'data': data
    }), status_code


# ── ROUTE 1: GET all courses ─────────────────────────────────────
@courses_bp.route('/', methods=['GET'])
def get_courses():
    return make_response_json(courses_list)


# ── ROUTE 2: POST create a new course ────────────────────────────
@courses_bp.route('/', methods=['POST'])
def create_course():
    global next_id

    # Read the JSON body sent by the user
    data = request.get_json()

    # Task 2: If no JSON was sent, return error
    if data is None:
        return jsonify({
            'status': 'error',
            'message': 'Please send JSON. Set Content-Type: application/json'
        }), 400

    # Task 2: Check all required fields are present
    required_fields = ['name', 'code', 'credits']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400

    # Build and save the new course
    course = {
        'id': next_id,
        'name': data['name'],
        'code': data['code'],
        'credits': data['credits']
    }
    courses_list.append(course)
    next_id += 1

    return make_response_json(course, 201)


# ── ROUTE 3: GET one course by id ────────────────────────────────
@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    # Search the list for a course with matching id
    course = next((c for c in courses_list if c['id'] == course_id), None)

    if course is None:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404

    return make_response_json(course)


# ── ROUTE 4: PUT update a course ─────────────────────────────────
@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = next((c for c in courses_list if c['id'] == course_id), None)

    if course is None:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404

    data = request.get_json()
    if data is None:
        return jsonify({'status': 'error', 'message': 'Please send JSON'}), 400

    # Only update fields that were actually sent
    if 'name' in data:
        course['name'] = data['name']
    if 'code' in data:
        course['code'] = data['code']
    if 'credits' in data:
        course['credits'] = data['credits']

    return make_response_json(course)


# ── ROUTE 5: DELETE a course ─────────────────────────────────────
@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    global courses_list

    course = next((c for c in courses_list if c['id'] == course_id), None)

    if course is None:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404

    # Remove course from list
    courses_list = [c for c in courses_list if c['id'] != course_id]

    return make_response_json({'message': f'Course {course_id} deleted'})