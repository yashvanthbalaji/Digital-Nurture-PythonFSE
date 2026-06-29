from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def hello_view(request):
    return HttpResponse('Course Management Api is Running')