from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(req):
    return HttpResponse('<h1>Welcome My Friends !</h1>')
# Create your views here.
