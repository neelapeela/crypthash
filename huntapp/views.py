from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
import operator

# Create your views here.

def home(request):
    return render(request, "index.html")