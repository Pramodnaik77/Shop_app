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
]