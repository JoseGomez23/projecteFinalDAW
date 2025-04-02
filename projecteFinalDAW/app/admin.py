from django.contrib import admin
from .models import GrupFamiliar, UsuarioGrupo, FavoriteProducts, ShoppingCartList, history
# Register your models here.
admin.site.register(GrupFamiliar)
admin.site.register(UsuarioGrupo)
admin.site.register(FavoriteProducts)
admin.site.register(ShoppingCartList)
admin.site.register(history)
