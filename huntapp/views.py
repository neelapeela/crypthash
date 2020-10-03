from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Progress, Level
import operator
import requests

# Create your views here.

def home(request):
    return render(request, 'index.html')
