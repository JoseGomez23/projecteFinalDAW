from django.urls import path
from . import views


urlpatterns = [

    path('register/', views.register, name="register"),  
    path('login/', views.login, name="login"),
    path('addGroupMember/', views.groups, name="addGroupMember"),
    path('createGroup/', views.createGroup, name="createGroup"),
    path('logout/', views.logout, name="logout")
]