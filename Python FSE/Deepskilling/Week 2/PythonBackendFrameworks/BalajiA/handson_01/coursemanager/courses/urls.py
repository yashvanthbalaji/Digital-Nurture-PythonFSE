from django.urls import path
from . import views

# URL patterns for the courses app
urlpatterns = [
    path('api/hello/', views.hello_view, name='hello'),
]