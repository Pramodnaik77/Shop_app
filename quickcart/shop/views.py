from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
import mysql.connector as sql
from math import ceil
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def index(request):
    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()
    q = "select * from category"
    cursor.execute(q)
    allprods = []
    t = tuple(cursor.fetchall())
    for j in range(len(t)):
        ml = t[j][0]
        c = "select * from Product where P_catid='{}'".format(ml)
        cursor.execute(c)
        tp = tuple(cursor.fetchall())
        dit = []
        for i in range(0, len(tp)):
            params = {'Pid': tp[i][0], 'Pname': tp[i][1], 'P_image': tp[i][2],
                      'P_desc': tp[i][3], 'P_brand': tp[i][4], 'P_price': tp[i][5]}
            dit.append(params)
        n = len(dit)
        cat = t[j][1]
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([dit, range(1, nslides), nslides, cat])

    l = []
    if request.user.is_authenticated:
        cust = request.user.email
        c = "select * from cart where cust_id='{}'".format(cust)
        cursor.execute(c)
        t = tuple(cursor.fetchall())

        for i in range(len(t)):
            l.append(t[i][1])

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
        us = authenticate(username=name, password=pwd)

        if us is not None:
            login(request, us)
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
        if request.user.is_authenticated:
            cust = request.user.email
            c = "select * from product where P_id='{}'".format(myid)
            cursor.execute(c)
            t = tuple(cursor.fetchall())
            d = {}
            c = "insert into cart values ('{}','{}','{}')".format(cust, t[0][0], 1)
            cursor.execute(c)
            m.commit()

            return redirect('/shop')
        else:
            messages.error(request, "Login to add the items to cart")
            return redirect('/shop')
    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()

    if request.user.is_authenticated:
        cust = request.user.email
        c = "select count(*) from cart where cust_id ='{}'".format(cust)
        cursor.execute(c)
        n = tuple(cursor.fetchall())
        if n != ():
            n = n[0][0]
        else:
            n = 0
        c = "select * from product p JOIN cart c on p.P_id=c.P_id and cust_id ='{}' ".format(cust)
        cursor.execute(c)
        t = tuple(cursor.fetchall())

        d = []
        total = 0
        if t != ():
            for i in range(0, len(t)):
                params = {'Pid': t[i][0], 'Pname': t[i][1], 'P_image': t[i][2],
                          'P_desc': t[i][3], 'P_brand': t[i][4], 'P_price': t[i][5],
                          'P_quantity': t[i][9]
                          }
                total += (t[i][9] * t[i][5])
                d.append(params)
    else:
        n = 0
        d = []
        total = 0

    if total > 1000:
        tot = total - 100
        dis = 100
    else:
        tot = total
        dis = 0

    return render(request, 'cart.html', {"len": n, "dict": d, "total": total, "tot": tot, "dis": dis})


def remove(request, myid):
    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()
    cust = request.user.email
    c = "delete from cart where P_id='{}' and cust_id='{}'".format(myid, cust)
    cursor.execute(c)
    m.commit()

    return redirect('/shop')


def search_items(request):
    if request.method == 'POST':
        desc1 = request.POST['desc1']
        # desc1 = desc1.lower()
        m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
        cursor = m.cursor()

        q = "select * from category"
        cursor.execute(q)
        allprods = []
        t = tuple(cursor.fetchall())
        for j in range(len(t)):
            ml = t[j][0]

            c = "select * from Product where P_catid='{}'".format(ml)
            cursor.execute(c)
            tp = tuple(cursor.fetchall())

            if tp != ():

                s = " "
                dit = []
                for i in range(0, len(tp)):
                    s = tp[i][1] + " " + tp[i][3] + " " + tp[i][4] + " " + str(tp[i][5])


                    if desc1.lower() in s.lower():
                        params = {'Pid': tp[i][0], 'Pname': tp[i][1], 'P_image': tp[i][2],
                                  'P_desc': tp[i][3], 'P_brand': tp[i][4], 'P_price': tp[i][5]}
                        dit.append(params)
                if dit != []:
                    n = len(dit)

                    cat = t[j][1]
                    nslides = n // 4 + ceil((n / 4) - (n // 4))
                    allprods.append([dit, range(1, nslides), nslides, cat])
        if allprods == []:
            messages.error(request, "No product found")
            return redirect('/shop')
        else:
            param = {'allprods': allprods, 'len': 1}
            return render(request, 'shop/index.html', param)


def order(request):
    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()

    cust = request.user.email
    c = "select * from product p JOIN cart c on p.P_id=c.P_id and cust_id ='{}' ".format(cust)
    cursor.execute(c)
    t = tuple(cursor.fetchall())
    d = []

    c = "select * from users where Email='{}'".format(cust)
    cursor.execute(c)
    us = tuple(cursor.fetchall())

    cus = us[0]
    customer = {'C_name': cus[0].capitalize(), 'C_Email': cus[2], 'C_Addr1': cus[3], 'C_city': cus[4], 'C_state': cus[5],
                'C_phone': cus[6]}

    total = 0
    if t != ():
        for i in range(0, len(t)):
            params = {'Pid': t[i][0], 'Pname': t[i][1].capitalize(), 'P_image': t[i][2],
                      'P_desc': t[i][3], 'P_brand': t[i][4], 'P_price': t[i][5], 'P_quantity': t[i][9]}
            total += (t[i][5] * t[i][9])
            d.append(params)
    if total > 1000:
        dis = 100
        total = total - 100
    else:
        dis = 0

    return render(request, 'order.html', {'dit': d, 'total': total, 'dis': dis, 'cust': customer})


def inc_item(request, myid):
    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()
    cust = request.user.email
    c = "select quantity from cart where P_id='{}' and cust_id='{}'".format(myid, cust)
    cursor.execute(c)
    t = tuple(cursor.fetchall())

    quantity = t[0][0] + 1
    c = "update cart set quantity='{}' where P_id='{}' and cust_id='{}'".format(quantity, myid, cust)
    cursor.execute(c)
    m.commit()
    return redirect('/shop/cart/9481')


def dec_item(request, myid):
    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()
    cust = request.user.email

    c = "select quantity from cart where P_id='{}' and cust_id='{}'".format(myid, cust)
    cursor.execute(c)
    t = tuple(cursor.fetchall())

    if t[0][0] > 1:
        quantity = t[0][0] - 1
        c = "update cart set quantity='{}' where P_id='{}' and cust_id='{}'".format(quantity, myid, cust)
        cursor.execute(c)
        m.commit()
    # else:
    #     messages.error(request, "")
    return redirect('/shop/cart/9481')


def change_address(request):
    if request.method == "POST":
        name2 = request.POST['name2']
        phone2 = request.POST['phone2']
        city2 = request.POST['city2']
        address2 = request.POST['address2']
        print(name2, phone2, city2, address2)
        return redirect('/shop/order')
