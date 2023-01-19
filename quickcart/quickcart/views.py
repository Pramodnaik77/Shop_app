from django.http import HttpResponse
from django.shortcuts import render, redirect
import mysql.connector as sql


# Create your views here.


def index(request):
    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()
    c = "create trigger IF NOT EXISTS order_backup " \
        "before delete on orders " \
        "for each row " \
        "begin " \
        "insert into order_history " \
        "values(old.ord_id,old.cust_id,old.C_name,sysdate(),old.C_phone," \
        "old.city,old.state,old.total,old.address,old.pincode); " \
        "end"
    cursor.execute(c)
    m.commit()
    return render(request, 'home.html')

