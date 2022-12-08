from django.http import HttpResponse
from django.shortcuts import render, redirect
import mysql.connector as sql

# Create your views here.


def index(request):
    return render(request, 'home.html')


