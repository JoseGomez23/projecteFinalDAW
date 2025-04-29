from django.urls import path
from . import views


urlpatterns = [

    path('register/', views.register, name="register"),  
    path('login/', views.login, name="login"),
    path('addGroupMember/<int:group_id>/', views.groups, name="addGroupMember"),
    path('qrCodeReader/', views.qrReader, name="qrCodeReader"),
    path('createGroup/', views.createGroup, name="createGroup"),
    path('addProductApi/', views.addProductApi, name="addProductApi"),
    path('logout/', views.logout, name="logout")
]