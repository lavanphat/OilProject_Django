from django.contrib import admin
from django.urls import path, include

from product import views

urlpatterns = [
    path('product', views.product, name='product'),
    path('service', views.service, name='service'),
]