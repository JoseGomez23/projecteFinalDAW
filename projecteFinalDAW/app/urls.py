from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name="index"),
    path('indexLogat/', views.indexLogat, name="indexLogat"),
    path('leaveGroup/', views.leaveGroup, name="leaveGroup"),
    path('acceptInvite/<int:group_id>/<str:invite_token>/', views.acceptInvite, name="acceptInvite"),
    path('subcategories/<int:categoria_id>/', views.subcategories, name="subcategories"),
    path('products/<int:categoria_id>/', views.products, name="products"),
    path('groups/', views.groups, name="groups")    
]