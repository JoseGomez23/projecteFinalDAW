from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UsuarioGrupo, GrupFamiliar, FavoriteProducts
from django.shortcuts import get_object_or_404
import requests
from django.http import JsonResponse
# Create your views here.


def index(request):
    
    url = "https://tienda.mercadona.es/api/categories/"
    response = requests.get(url)
    
    title = "Categories"

    if response.status_code == 200:
        data = response.json() 
        categorias = data.get("results", [])  
    else:
        categorias = []

    return render(request, "indexLogat.html", {"categories": categorias, "title": title})

def subcategories(request, categoria_id):
    url = "https://tienda.mercadona.es/api/categories/"
    response = requests.get(url)
    
    title = "Subcategories"

    if response.status_code == 200:
        data = response.json().get("results", [])  
        subcategorias = []

        for categoria in data:
            if categoria["id"] == categoria_id:
                subcategorias = categoria.get("categories", [])  
                break
    else:
        subcategorias = []

    return render(request, "categories.html", {"categories": subcategorias, "title": title})

def products(request, categoria_id):
    url = f"https://tienda.mercadona.es/api/categories/{categoria_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  
        products = []
       
        for subcategoria in data.get("categories", []):
            for producto in subcategoria.get("products", []): 
                if producto.get("published", False): 
                    products.append(producto)  
    else:
        products = []
        
    favorites = []
    
    if request.user.is_authenticated:    
        favorites = FavoriteProducts.objects.filter(user=request.user).values_list("product_id", flat=True)


    return render(request, "products.html", {"products": products, "favorites": favorites})
    
    

@login_required
def groups(request):
    try:
        userGroup = UsuarioGrupo.objects.get(user=request.user)
        group = userGroup.group
        members = group.members.all()
    except UsuarioGrupo.DoesNotExist:
        group = None
        members = None

    return render(request, 'grups.html', {'group': group, 'members': members})

@login_required
def leaveGroup(request):
    try:
        userGroup = UsuarioGrupo.objects.get(user=request.user)
        group = userGroup.group
        userGroup.delete()
        
        if not UsuarioGrupo.objects.filter(group=group).exists():
            group.delete()

        return redirect('groups') 

    except UsuarioGrupo.DoesNotExist:
        return redirect('groups')  

def acceptInvite(request, group_id, invite_token):
    if not request.user.is_authenticated:
        return render(request, 'acceptInvite.html', {'error': 'Has d\'estar autenticat per acceptar la invitació!'})

    group = get_object_or_404(GrupFamiliar, id=group_id)

    
    if UsuarioGrupo.objects.filter(user=request.user, group=group).exists():
        return render(request, 'acceptInvite.html', {'error': 'Ja ets membre d\'aquest grup!'})

    UsuarioGrupo.objects.create(user=request.user, group=group)

    return render(request, 'acceptInvite.html', {'message': 'Has estat afegit al grup correctament!'})

@login_required
def addFavorite(request, product_id):
    
    url = f"https://tienda.mercadona.es/api/products/{product_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
    name = data.get("display_name", "")
    price = data.get("unit_price", 0)
    old_price = data.get("price_instructions.previous_unit_price", 0)
    image = data.get("thumbnail", "")
    
    #print(name)
    #print(image)
    
    price_info = data.get("price_instructions", {})
    price = price_info.get("unit_price", 0)
    old_price = price_info.get("previous_unit_price", 0)
    
    print(price)
    #print(old_price)
    
    if request.method == "POST":
        favorite, created = FavoriteProducts.objects.get_or_create(user=request.user, product_id=product_id, name=name, image=image, price=price, old_price=old_price)
        return JsonResponse({"message": "Añadido a favoritos" if created else "Ya estaba en favoritos"})
    return JsonResponse({"error": "Método no permitido"}, status=405)
    
    

@login_required
def showFavorites(request):
    
    favorites = FavoriteProducts.objects.filter(user=request.user)
    products = []

    for favorite in favorites:
        products.append({
            "id": favorite.product_id,
            "name": favorite.name,
            "price": favorite.price,
            "old_price": favorite.old_price,
            "image": favorite.image
        })

    return render(request, "favorites.html", {"products": products})

@login_required
def removeFavorites(request, product_id):
    if request.method == "POST":
        try:
            favorite = FavoriteProducts.objects.get(user=request.user, product_id=product_id)
            favorite.delete()
            return JsonResponse({"message": "Eliminado de favoritos"})
        except FavoriteProducts.DoesNotExist:
            return JsonResponse({"error": "El producto no estaba en favoritos"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

