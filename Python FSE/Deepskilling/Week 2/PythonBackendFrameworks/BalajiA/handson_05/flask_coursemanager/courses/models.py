from extensions import db

# Department model — one department has many courses
class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    head_of_dept = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Numeric(10, 2), nullable=False)

    # One department → many courses
    courses = db.relationship('Course', back_populates='department')

    # to_dict() converts this object into a plain Python dict
    # so we can send it as JSON (Flask's version of DRF serializer)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'head_of_dept': self.head_of_dept,
            'budget': float(self.budget)
        }

    def __repr__(self):
        return f'<Department {self.name}>'


# Course model — belongs to one department
class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    # ForeignKey links this course to a department
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    # Relationships
    department = db.relationship('Department', back_populates='courses')
    enrollments = db.relationship('Enrollment', back_populates='course')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'credits': self.credits,
            'department_id': self.department_id
        }

    def __repr__(self):
        return f'<Course {self.name}>'


# Student model
class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    enrollment_year = db.Column(db.Integer, nullable=False)

    enrollments = db.relationship('Enrollment', back_populates='student')

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'enrollment_year': self.enrollment_year
        }

    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'


# Enrollment model — links students to courses
class Enrollment(db.Model):
    __tablename__ = 'enrollment'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)
    grade = db.Column(db.String(2), nullable=True)

    student = db.relationship('Student', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'enrollment_date': str(self.enrollment_date),
            'grade': self.grade
        }

    def __repr__(self):
        return f'<Enrollment {self.student_id} - {self.course_id}>'