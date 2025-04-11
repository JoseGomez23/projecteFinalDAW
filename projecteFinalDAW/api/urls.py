from django.urls import path
from . import views

urlpatterns = [


    path('add_product/', views.addProduct, name='add_product'),
]

