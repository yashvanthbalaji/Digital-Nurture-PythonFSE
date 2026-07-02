from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# OWNS its own database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///course_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#  MODELS 
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    head_of_dept = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'head_of_dept': self.head_of_dept}


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name,
            'code': self.code, 'credits': self.credits,
            'department_id': self.department_id
        }


# Create tables on startup
with app.app_context():
    db.create_all()


# ── ROUTES
@app.route('/api/courses/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses])


@app.route('/api/courses/', methods=['POST'])
def create_course():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON required'}), 400
    for field in ['name', 'code', 'credits', 'department_id']:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    course = Course(
        name=data['name'], code=data['code'],
        credits=data['credits'], department_id=data['department_id']
    )
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201


@app.route('/api/courses/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': f'Course {course_id} not found'}), 404
    return jsonify(course.to_dict())


@app.route('/api/courses/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    db.session.delete(course)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    # Runs on port 5001 — 
    app.run(port=5001, debug=True)