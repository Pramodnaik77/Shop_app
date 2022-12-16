from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
import mysql.connector as sql


# Create your views here.
def index(request):
    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()
    c = "select * from Product"
    cursor.execute(c)
    t = tuple(cursor.fetchall())
    d = []#{}
    for i in range(0, len(t)):
        params = {'Pid': t[i][0], 'Pname': t[i][1], 'P_image': t[i][2], 'P_desc': t[i][3], 'P_brand': t[i][4], 'P_price': t[i][5]}
        #d[i] = params

        d.append(params)
    # for i in range(2):
    #     print(d[i]['Pname'])
    #
    # params = {'Pid': t[1][0], 'P_name': t[1][1], 'P_image': t[1][2], 'P_desc': t[1][3], 'P_brand': t[1][4],
    #           'P_price': t[1][5]}
    #
    # print(params)
    # params = {'range': range(4), 'dit': params}

    return render(request, 'shop/index.html', {'range': range(4), 'dit': d})


def register(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        adrs = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        # print(name, password, email, adrs, city, state, phone)
        m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
        cursor = m.cursor()
        c = "insert into users values ( '{}','{}','{}','{}','{}','{}','{}' )".format(name, password, email, adrs, city,
                                                                                     state, phone)
        cursor.execute(c)
        m.commit()
        return redirect('/')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        pwd = request.POST.get('password', '')
        # print(name)
        # print(pwd)

        m = sql.connect(host="localhost", user="root", password="Pramod@12", database="register")
        cursor = m.cursor()

        c = "select * from users where Name ='{}' and  Password = '{}' ".format(name, pwd)
        cursor.execute(c)

        t = tuple(cursor.fetchall())
        if t == ():
            return redirect('/shop/login/')
        else:
            return redirect('/shop/')

    else:
        return render(request, 'login.html')


def contact(request):
    if request.method == "POST":
        redirect('/shop/conatct/')

    return render(request, 'contact.html')


def cart(request):
    return render(request, 'cart.html')


def about(request):
    return render(request, 'about.html')
