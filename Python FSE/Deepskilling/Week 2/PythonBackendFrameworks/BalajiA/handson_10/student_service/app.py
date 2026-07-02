from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests as http_client   # renamed to avoid clash with Flask's request
from datetime import date

app = Flask(__name__)

# OWNS its own database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Course Service
COURSE_SERVICE_URL = 'http://127.0.0.1:5001'


# ── MODELS 
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    enrollment_year = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id, 'first_name': self.first_name,
            'last_name': self.last_name, 'email': self.email,
            'enrollment_year': self.enrollment_year
        }


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    enrollment_date = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id, 'student_id': self.student_id,
            'course_id': self.course_id, 'enrollment_date': self.enrollment_date
        }


with app.app_context():
    db.create_all()


#  ROUTES 
@app.route('/api/students/', methods=['GET'])
def get_students():
    return jsonify([s.to_dict() for s in Student.query.all()])


@app.route('/api/students/', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON required'}), 400
    for field in ['first_name', 'last_name', 'email', 'enrollment_year']:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    student = Student(
        first_name=data['first_name'], last_name=data['last_name'],
        email=data['email'], enrollment_year=data['enrollment_year']
    )
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


@app.route('/api/students/<int:student_id>/', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student.to_dict())


#  ENROLLMENT ROUTE — calls Course Service 
@app.route('/api/students/<int:student_id>/enroll', methods=['POST'])
def enroll_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    data = request.get_json()
    if not data or 'course_id' not in data:
        return jsonify({'error': 'course_id is required'}), 400

    course_id = data['course_id']

    # ── INTER-SERVICE CALL 
    # Student Service asks Course Service: does this course exist?
    # This is synchronous HTTP communication between services.
    try:
        response = http_client.get(
            f'{COURSE_SERVICE_URL}/api/courses/{course_id}/',
            timeout=5   # fail fast if service is slow
        )
        if response.status_code == 404:
            return jsonify({'error': f'Course {course_id} not found'}), 404
        if response.status_code != 200:
            return jsonify({'error': 'Course Service returned an error'}), 502

    except http_client.ConnectionError:
        return jsonify({
            'error': 'Course Service is unavailable. Please try again later.',
            'code': 'SERVICE_UNAVAILABLE'
        }), 503

    except http_client.Timeout:
        return jsonify({'error': 'Course Service timed out'}), 503

    enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id,
        enrollment_date=str(date.today())
    )
    db.session.add(enrollment)
    db.session.commit()

    return jsonify({
        'message': f'{student.first_name} enrolled in course {course_id}',
        'enrollment': enrollment.to_dict()
    }), 201


if __name__ == '__main__':
    app.run(port=5002, debug=True)