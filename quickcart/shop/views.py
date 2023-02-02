from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
import mysql.connector as sql
from math import ceil
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date
from django.http import HttpResponseRedirect
import shutil
from .models import ImageModel


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
    if request.method == "POST":
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        adrs = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        pincode = request.POST.get('pincode', '')
        f = -1
        m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
        cursor = m.cursor()
        try:
            isexits = User.objects.get(username=name)
            f = 1
            l = "select * from users where Name = '{}'".format(isexits)
            cursor.execute(l)
            em = tuple(cursor.fetchall())
            if em == ():
                isexits.delete()
                f = 0
        except:
            f = 2
            user = User.objects.create_user(name, email, password)
            user.save()

        l = "select * from users where Phone='{}' or Email='{}'".format(phone, email)
        cursor.execute(l)
        p = tuple(cursor.fetchall())

        if p != () or f == 1:
            messages.error(request, 'Email already exists')
            return redirect('/shop/register')
        c = "insert into users values ( '{}','{}','{}','{}','{}','{}','{}','{}' )".format(name, password, email, adrs,
                                                                                          city,
                                                                                          state, phone, pincode)
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
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        city = request.POST["city"]
        state = request.POST["state"]
        pincode = request.POST["pincode"]
        feedback_desc = request.POST["desc"]
        m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
        cursor = m.cursor()
        c = "insert into contact_us values ( '{}','{}','{}','{}','{}','{}','{}','{}' )".format(name, email, address,
                                                                                               city,
                                                                                               state,
                                                                                               phone, pincode,
                                                                                               feedback_desc)
        cursor.execute(c)
        m.commit()
        messages.success(request, "Your feedback submitted successfully")
        return redirect('/shop')

    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def prod_view(request, myid):
    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()
    c = "select * from product where P_id='{}'".format(myid)
    cursor.execute(c)
    t = tuple(cursor.fetchall())
    d = {}
    for i in range(0, 1):
        d = {'Pid': t[i][0], 'Pname': t[i][1], 'P_image': t[i][2], 'P_desc': t[i][3],
             'P_brand': t[i][4], 'P_price': t[i][5]}
    l = []
    rev = {}
    r_exist = False
    oth_exist = False
    oth_rev = []
    if request.user.is_authenticated:
        cust = request.user.email
        c = "select * from cart where cust_id='{}'".format(cust)
        cursor.execute(c)
        t = tuple(cursor.fetchall())

        for i in range(len(t)):
            l.append(t[i][1])

        c = "select * from reviews where cust_id='{}' and prod_id ='{}'".format(cust, myid)
        cursor.execute(c)
        top_rev = tuple(cursor.fetchall())
        c = "select * from reviews where prod_id='{}' and cust_id != '{}'".format(myid, cust)
        cursor.execute(c)
        other_rev = tuple(cursor.fetchall())
        r_exist=True
        i = 0
        oth_rev = []
        oth_exist = False
        if other_rev != ():
            oth_exist = True
            for rat in other_rev:
                if i < 2:
                    rev = {'P_name': other_rev[i][1], 'P_desc': other_rev[i][2], 'P_star': other_rev[i][3]}
                    oth_rev.append(rev)
                else:
                    break
                i += 1

        if top_rev != ():
            r_exist = True
            for i in range(len(top_rev)):
                rev = {'P_name': top_rev[0][1], 'P_desc': top_rev[0][2], 'P_star': top_rev[0][3]}
        else:
            r_exist = False

    return render(request, 'prodview.html', {'dict': d, 'len': l, 'rev': rev, 'r_exist': r_exist,
                                             'range': range(0, 5), 'oth_exist': oth_exist, 'oth_rev': oth_rev})


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
    # c = "delete from cart where P_id='{}' and cust_id='{}'".format(myid, cust)
    # cursor.execute(c)
    c = "call remove_from_cart('{}','{}')".format(cust, myid)
    cursor.execute(c)
    m.commit()

    return redirect('/shop')


def search_items(request):
    if request.method == 'POST':
        desc1 = request.POST['desc1']
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
                    s = tp[i][1] + " " + tp[i][3] + " " + tp[i][4] + " " + str(tp[i][5]) + " " + t[j][1]

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
    c = "select * from users where Email ='{}'".format(cust)
    cursor.execute(c)
    us1 = tuple(cursor.fetchall())

    c = "select * from orders where cust_id='{}'".format(cust)

    cursor.execute(c)
    us = tuple(cursor.fetchall())

    if us == ():
        c = "insert into orders(cust_id,C_name,ord_date,C_phone,city,state,address,pincode)" \
            " values('{}','{}',sysdate(),'{}','{}','{}','{}','{}')".format(cust,
                                                                           us1[0][0],
                                                                           us1[0][6], us1[0][4],
                                                                           us1[0][5],
                                                                           us1[0][3], us1[0][7])
        cursor.execute(c)
        m.commit()
        c = "select * from orders where cust_id='{}'".format(cust)
        cursor.execute(c)
        us = tuple(cursor.fetchall())

    c = "select * from product p JOIN cart c on p.P_id=c.P_id and cust_id ='{}' ".format(cust)
    cursor.execute(c)
    t = tuple(cursor.fetchall())
    d = []

    cus = us[0]
    customer = {'C_name': cus[2].capitalize(), 'C_Email': cus[1], 'C_Addr1': cus[8], 'C_city': cus[5],
                'C_state': cus[6],
                'C_phone': cus[4], 'ord_id': cus[0]}

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
    c = "update orders set total='{}'where cust_id='{}'".format(total, cust)
    cursor.execute(c)
    m.commit()
    quant = 8
    return render(request, 'order.html', {'dit': d, 'total': total, 'dis': dis, 'cust': customer, 'quant': quant})


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
    return redirect('/shop/cart/9481')


def change_address(request):
    if request.method == "POST":
        m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
        cursor = m.cursor()
        cust = request.user.email
        name2 = request.POST['name2']
        phone2 = request.POST['phone2']
        city2 = request.POST['city2']
        address2 = request.POST['address2']
        pincode2 = request.POST['pincode2']

        c = "update orders set cust_id='{}',C_name='{}',ord_date='{}',C_phone='{}'," \
            "city='{}',address='{}',pincode='{}' where cust_id='{}'".format(cust,
                                                                            name2,
                                                                            date.today(),
                                                                            phone2, city2,
                                                                            address2, pincode2, cust)
        cursor.execute(c)
        m.commit()
        return redirect('/shop/order')


def order_complete(request):
    messages.success(request, "Order placed successfully")
    us = request.user.email
    m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
    cursor = m.cursor()
    c = "select ord_id from orders where cust_id='{}'".format(us)
    cursor.execute(c)
    l = cursor.fetchall()
    ord_id = l[0][0]
    c = "insert into order_items SELECT '{}',P_id,quantity from cart where cust_id = '{}' ".format(ord_id, us)
    cursor.execute(c)
    c = "call delete_cart('{}')".format(us)
    cursor.execute(c)
    # c = "delete from cart where cust_id = '{}'".format(us)
    # cursor.execute(c)
    # c = "delete from orders where cust_id='{}'".format(us)
    # cursor.execute(c)
    m.commit()

    return redirect('/shop')


def buy_now(request, myid):
    if request.user.is_authenticated:

        m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
        cursor = m.cursor()
        cust = request.user.email
        c = "select * from cart where P_id='{}' and cust_id='{}'".format(myid, cust)
        cursor.execute(c)
        pd = tuple(cursor.fetchall())
        if pd == ():
            c = "select * from product where P_id='{}'".format(myid)
            cursor.execute(c)
            t = tuple(cursor.fetchall())
            d = {}
            c = "insert into cart values ('{}','{}','{}')".format(cust, t[0][0], 1)
            cursor.execute(c)
            m.commit()

        return redirect('/shop/cart/9481')
    else:
        messages.error(request, "Login to Buy items")
        return redirect('/shop')


def review_star(request, myid):
    if request.method == "POST":
        if request.user.is_authenticated:
            m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
            cursor = m.cursor()
            cust = request.user.email
            rev_desc = request.POST['rev_desc']
            rev_star = request.POST['rev_star']
            us_name = request.user.username
            c = "insert into reviews values('{}','{}','{}','{}','{}')".format(cust, us_name,
                                                                              rev_desc, rev_star, myid)
            cursor.execute(c)
            m.commit()

            return redirect('/shop/prodview/' + str(myid))

        messages.error(request, "Login to add reviews")
        return redirect('/shop')


def order_history(request):
    if request.user.is_authenticated:
        m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
        cursor = m.cursor()
        cust = request.user.email
        c = "select * from order_history where cust_id='{}'".format(cust)
        cursor.execute(c)
        t = tuple(cursor.fetchall())
        dit = []
        item_ordered = False
        if t != ():
            item_ordered = True

            add = 0
            for tup in t:
                tup[0]
                params = {'ord_id': tup[0], 'cust_id': tup[1], 'c_name': tup[2], 'ord_date': tup[3], 'c_phone': tup[4],
                          'city': tup[5], 'state': tup[6], 'total': tup[7], 'address': tup[8], 'pincode': tup[9]}
                c = "select p.P_name,o.quantity from order_items o, product p where " \
                    "o.ord_id='{}' and p.P_id = o.P_id".format(tup[0])
                cursor.execute(c)
                prod = cursor.fetchall()
                ord_item = []
                for p in prod:
                    ord_item.append([p[0], p[1]])
                dit.append([params, ord_item])
        return render(request, 'order_history.html', {'dict': dit, 'ord_exist': item_ordered})
    messages.error(request, "Login to view your order history!!!!")
    return redirect('/shop')


def admin_page(request):
    if request.method == 'POST':
        m = sql.connect(host="localhost", user="root", passwd="Pramod@12", database="register")
        cursor = m.cursor()

        P_id = request.POST['Pid']
        P_name = request.POST['Pname']
        P_desc = request.POST['desc']
        P_brand = request.POST['P_brand']
        P_price = request.POST['Price']
        P_catid = request.POST['cat_id']
        P_quantity = request.POST['quantity']

        files = request.FILES
        image = files.get("image")
        P_image = 'shop/uploads/' + str(image)

        instance = ImageModel()
        instance.image = image
        instance.save()
        c = "insert into product values ('{}','{}','{}','{}','{}','{}','{}')".format(P_id, P_name.upper(), P_image,
                                                                                     P_desc, P_brand, P_price, P_catid)
        cursor.execute(c)
        m.commit()

    return render(request, 'admin_page.html')
