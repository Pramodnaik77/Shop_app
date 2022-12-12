from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name='shop'),
    path("contact/", views.contact, name="contact"),
    # path('about/', views.about, name="about"),
    path('cart/', views.cart, name="cart"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
]