from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name="index"),
    path('indexLogat/', views.index, name="indexLogat"),
    path('leaveGroup/<int:group_id>/', views.leaveGroup, name="leaveGroup"),
    path('acceptInvite/<int:group_id>/<str:invite_token>/', views.acceptInvite, name="acceptInvite"),
    path('subcategories/<int:categoria_id>/', views.subcategories, name="subcategories"),
    path('products/<int:categoria_id>/', views.products, name="products"),
    path('products/<int:categoria_id>/<int:group_id>/', views.products, name="products"),
    path("addFavorite/<int:product_id>/", views.addFavorite , name="addFavorite"),
    path("addGroupFavorite/<int:product_id>/<int:group_id>/", views.addFavorite , name="addGroupFavorite"),
    path("removeFavorite/<int:product_id>/", views.removeFavorites , name="removeFavorite"),
    path("removeGroupFavorite/<int:product_id>/<int:group_id>/", views.removeFavorites , name="removeGroupFavorite"),
    path('favorites/', views.showFavorites, name="favorites"),
    path('favorites/<int:group_id>/', views.showFavorites, name="favorites"),
    path('addProductToList/<int:product_id>/', views.addProductToList, name="addProductToList"),
    path('addProductToList/<int:product_id>/<int:group_id>/', views.addProductToList, name="addProductToList"),
    path('shoppingCartList/', views.shoppingCartList, name="shoppingCartList"),
    path('shoppingCartList/<int:group_id>/', views.shoppingCartList, name="shoppingCartList"),
    path('addOneProduct/<int:product_id>/' , views.addOneProduct, name="addOneProduct"),
    path('addOneProduct/<int:product_id>/<int:group_id>/' , views.addOneProduct, name="addOneProductGroups"),
    path('removeOneProduct/<int:product_id>/' , views.removeOneProduct, name="removeOneProduct"),
    path('removeOneProduct/<int:product_id>/<int:group_id>/' , views.removeOneProduct, name="removeOneProductGroups"),
    path('removeProduct/<int:product_id>/' , views.removeProductFromList, name="removeProduct"),
    path('removeProduct/<int:product_id>/<int:group_id>/' , views.removeProductFromList, name="removeProductGroups"),
    path('removeChecked/<str:group_id>/', views.removeChecked, name="removeCheckedProducts"),
    path('history/', views.history, name="history"),
    path('addFromHistory/<int:product_id>/<str:ticket_id>/', views.addFromHistory, name="addFromHistory"),
    path('groups/', views.groups, name="groups")    
]

