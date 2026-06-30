from rest_framework import serializers
from .models import Department, Course, Student, Enrollment

# A Serializer converts Python model objects into JSON
# and validates incoming JSON data before saving to DB
# ModelSerializer auto-reads all fields from the model

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'   # include every field

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'