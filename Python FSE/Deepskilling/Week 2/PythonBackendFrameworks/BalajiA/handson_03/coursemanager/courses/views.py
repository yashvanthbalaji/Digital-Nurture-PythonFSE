from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Student, Enrollment
from .serializers import CourseSerializer, StudentSerializer, EnrollmentSerializer

#  handson_01
def hello_view(request):
    return HttpResponse('Course Management API is running')



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # Custom action: GET /api/courses/1/students/
    # The @action decorator adds an extra endpoint to this viewset
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        # Get the course by its id
        course = get_object_or_404(Course, pk=pk)
        # Find all enrollment records for this course
        enrollments = Enrollment.objects.filter(course=course)
        # Get just the student from each enrollment
        enrolled_students = [e.student for e in enrollments]
        serializer = StudentSerializer(enrolled_students, many=True)
        return Response(serializer.data)

# Same pattern for Student — all CRUD in 3 lines
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# Same pattern for Enrollment
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer