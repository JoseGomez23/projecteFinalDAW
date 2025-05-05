from django.urls import path
from . import views

urlpatterns = [

    path('', views.getProducts, name='getProducts'),
    path('name=<str:name>/', views.getProduct, name='getProduct'),
    path('price=<str:price>/', views.getProductP, name='getProductP'),
    path('priceHigher=<str:price>/', views.getProductHigher, name='getProductPHigher'),
    path('priceLower=<str:price>/', views.getProductPLower, name='getProductPLower'),
    path('withDiscount=<str:boolean>/', views.getProductWithDiscount, name='getProductWithDiscount'),
]

