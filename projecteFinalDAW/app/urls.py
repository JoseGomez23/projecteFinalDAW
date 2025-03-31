from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name="index"),
    path('indexLogat/', views.index, name="indexLogat"),
    path('leaveGroup/', views.leaveGroup, name="leaveGroup"),
    path('acceptInvite/<int:group_id>/<str:invite_token>/', views.acceptInvite, name="acceptInvite"),
    path('subcategories/<int:categoria_id>/', views.subcategories, name="subcategories"),
    path('products/<int:categoria_id>/', views.products, name="products"),
    path("addFavorite/<int:product_id>/", views.addFavorite , name="addFavorite"),
    path("removeFavorite/<int:product_id>/", views.removeFavorites , name="removeFavorite"),
    path('favorites/', views.showFavorites, name="favorites"),
    path('addProductToList/<int:product_id>/', views.addProductToList, name="addProductToList"),
    path('shoppingCartList/', views.shoppingCartList, name="shoppingCartList"),
    path('addOneProduct/<int:product_id>/' , views.addOneProduct, name="addOneProduct"),
    path('removeOneProduct/<int:product_id>/' , views.removeOneProduct, name="removeOneProduct"),
    path('removeProduct/<int:product_id>/' , views.removeProductFromList, name="removeProduct"),
    path('removeChecked/', views.removeChecked, name="removeCheckedProducts"),
    path('groups/', views.groups, name="groups") 
]

