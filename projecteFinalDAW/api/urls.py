from django.urls import path
from . import views

urlpatterns = [

    path('', views.getProducts, name='getProducts'),
    path('<str:name>/', views.getProduct, name='getProduct'),
    path('add_product/', views.addProduct, name='add_product'),
]

