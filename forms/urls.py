from django.urls import path
from . import views


urlpatterns = [

    path('register/', views.register, name="register"),  
    path('login/', views.login, name="login"),
    path('addGroupMember/<int:group_id>/', views.groups, name="addGroupMember"),
    path('qrCodeReader/', views.qrReader, name="qrCodeReader"),
    path('createGroup/', views.createGroup, name="createGroup"),
    path('addProductApi/', views.addProductApi, name="addProductApi"),
    path('sendEmail/', views.sendEmail , name="sendEmail"),
    path('resetPassword/<str:token>', views.resetPassword, name="resetPassword"),
    path('manualResetPassword/', views.manualResetPwd, name="manualResetPassword"),
    path('logout/', views.logout, name="logout")
]