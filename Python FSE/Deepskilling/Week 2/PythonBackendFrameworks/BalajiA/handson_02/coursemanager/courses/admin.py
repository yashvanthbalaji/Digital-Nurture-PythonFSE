from django.contrib import admin
from .models import Department, Course, Student, Enrollment

admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Enrollment)

# i am creating Advanced registration for the Course model for better view
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'credits', 'department']
    search_fields = ['name', 'code']
    list_filter = ['department'] 

admin.site.register(Course,CourseAdmin)