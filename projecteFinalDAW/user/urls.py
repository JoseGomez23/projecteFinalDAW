from django.urls import path
from . import views

urlpatterns = [

    path('configuration/', views.configuration, name="configuration"),
]


