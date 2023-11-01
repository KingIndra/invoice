from django.urls import path
from django.contrib import admin
from app import views

urlpatterns = [
    path('send_invoice/', views.send_invoice, name='send_invoice'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
]
