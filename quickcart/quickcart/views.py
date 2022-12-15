from django.http import HttpResponse
from django.shortcuts import render, redirect
# import mysql.connector as sql

# Create your views here.


def index(request):
    # m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    # cursor = m.cursor()
    # c = "select * from Product where P_id = '{}'".format(104)
    # cursor.execute(c)
    # t = tuple(cursor.fetchall())
    # print(t[0][2])
    # {'abc': t[0][2]}
    return render(request, 'home.html')



