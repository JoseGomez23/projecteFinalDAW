from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name="index"),
    path('indexLogat/', views.indexLogat, name="indexLogat"),
    path('leaveGroup/', views.leaveGroup, name="leaveGroup"),
    path('acceptInvite/<int:group_id>/<str:invite_token>/', views.acceptInvite, name="acceptInvite"),
    path('groups/', views.groups, name="groups")    
]