from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='shop'),
    path("contact/", views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('cart/<int:myid>', views.cart, name="cart"),
    path('remove/<int:myid>', views.remove, name="remove"),
    path('register/', views.register, name="register"),
    path('login_check/', views.login_check, name="login_check"),
    path('logout_check/', views.logout_check, name="logout_check"),
    path('search_items/', views.search_items, name="search_items"),
    path('prodview/<int:myid>', views.prod_view, name="prod_view"),
    path('order/', views.order, name="order"),
    path('inc_item/<int:myid>', views.inc_item, name="inc_item"),
    path('dec_item/<int:myid>', views.dec_item, name="dec_item"),
    path('change_address/', views.change_address, name="change_address"),
    path('order_complete/', views.order_complete, name="order_complete"),
    path('buy_now/<int:myid>', views.buy_now, name="buy_now"),
    path('review_star/<int:myid>', views.review_star, name="review_star"),
    path('order_history', views.order_history, name="order_history"),
    path('admin_page/', views.admin_page, name="admin_page"),
]
