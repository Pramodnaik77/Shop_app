from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
import mysql.connector as sql
from math import ceil
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()
    c = "select * from Product"
    cursor.execute(c)
    t = tuple(cursor.fetchall())
    dit = []

    for i in range(0, len(t)):
        params = {'Pid': t[i][0], 'Pname': t[i][1], 'P_image': t[i][2],
                  'P_desc': t[i][3], 'P_brand': t[i][4], 'P_price': t[i][5]}
        dit.append(params)
    l = []
    c = "select * from cart"
    cursor.execute(c)
    t = tuple(cursor.fetchall())

    for i in range(len(t)):
        l.append(t[i][1])
    n = len(t)
    # print(l)
    nslides = n // 4 + ceil((n / 4) - (n // 4))
    allprods = [[dit, range(1, nslides), nslides], [dit, range(1, nslides), nslides]]
    param = {'allprods': allprods, 'len': l}
    return render(request, 'shop/index.html', param)


def register(request):
    # messages.success(request, "Welcome!! This is registration page")
    if request.method == "POST":
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        adrs = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        user = User.objects.create_user(name, email, password)
        user.save()
        m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
        cursor = m.cursor()
        l = "select * from users where Phone='{}' or Email='{}'".format(phone, email)
        cursor.execute(l)
        p = tuple(cursor.fetchall())

        if p != ():
            messages.error(request, 'Email already exists')
            return redirect('/shop/register')
        c = "insert into users values ( '{}','{}','{}','{}','{}','{}','{}' )".format(name, password, email, adrs,
                                                                                     city,
                                                                                     state, phone)
        cursor.execute(c)
        m.commit()
        messages.success(request, 'Registration successful')
        return redirect('/shop/login_check')
    else:
        return render(request, 'register.html')


def login_check(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        pwd = request.POST.get('password', '')

        m = sql.connect(host="localhost", user="root", password="Pramod@12", database="register")
        cursor = m.cursor()

        c = "select * from users where Name ='{}' and  Password = '{}' ".format(name, pwd)
        cursor.execute(c)

        t = tuple(cursor.fetchall())
        user = authenticate(username=name, password=pwd)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('shop')

        else:
            messages.error(request, "Wrong password or user_id")
            return redirect('/shop/login_check/')

    return render(request, 'login.html')


def logout_check(request):
    logout(request)

    return redirect('/')


def contact(request):
    if request.method == "POST":
        redirect('/shop/conatct/')

    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def prod_view(request, myid):
    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()
    c = "select * from product where P_id='{}'".format(myid)
    cursor.execute(c)
    t = tuple(cursor.fetchall())
    # d = []
    d = {}
    for i in range(0, 1):
        d = {'Pid': t[i][0], 'Pname': t[i][1], 'P_image': t[i][2], 'P_desc': t[i][3],
             'P_brand': t[i][4], 'P_price': t[i][5]}

    return render(request, 'prodview.html', {'dict': d})


def cart(request, myid):
    if myid != 9481:
        m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
        cursor = m.cursor()
        c = "select * from product where P_id='{}'".format(myid)
        cursor.execute(c)
        t = tuple(cursor.fetchall())

        d = {}
        c = "insert into cart values ( null,'{}','{}')".format(t[0][0], 1)
        cursor.execute(c)
        m.commit()
        return redirect('/shop')

    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()
    # c = "select * from cart"
    # cursor.execute(c)
    # l = tuple(cursor.fetchall())

    c = "select count(*) from cart"
    cursor.execute(c)
    n = tuple(cursor.fetchall())
    if n != ():
        n = n[0][0]
    else:
        n = 0
    c = "select * from product p JOIN cart c on p.P_id=c.P_id "
    cursor.execute(c)
    t = tuple(cursor.fetchall())

    d = []
    if t != ():
        for i in range(0, len(t)):
            params = {'Pid': t[i][0], 'Pname': t[i][1], 'P_image': t[i][2],
                      'P_desc': t[i][3], 'P_brand': t[i][4], 'P_price': t[i][5]}
            d.append(params)
    return render(request, 'cart.html', {"len": n, "dict": d})


def remove(request, myid):
    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()
    c = "delete from cart where P_id='{}'".format(myid)
    cursor.execute(c)
    m.commit()

    return redirect('/shop')


def search_items(request):
    if request.method == 'POST':
        desc1 = request.POST['desc1']
        desc1=desc1.lower()
        m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
        cursor = m.cursor()
        c = "select * from Product where P_name='{}' or P_desc like '{}' or P_brand='{}' or P_price='{}'".format(desc1,desc1,desc1,desc1)
        cursor.execute(c)
        t = tuple(cursor.fetchall())

        if t != ():
            dit = []

            for i in range(0, len(t)):
                params = {'Pid': t[i][0], 'Pname': t[i][1], 'P_image': t[i][2],
                          'P_desc': t[i][3], 'P_brand': t[i][4], 'P_price': t[i][5]}
                dit.append(params)
            l = []
            c = "select * from cart"
            cursor.execute(c)
            t = tuple(cursor.fetchall())

            for i in range(len(t)):
                l.append(t[i][1])
            n = len(t)
            # print(l)
            nslides = n // 4 + ceil((n / 4) - (n // 4))
            allprods = [[dit, range(1, nslides), nslides], [dit, range(1, nslides), nslides]]
            param = {'allprods': allprods, 'len': l}
            return render(request, 'shop/index.html', param)
        else:
            messages.error(request, "No product found")
            return redirect('/shop')