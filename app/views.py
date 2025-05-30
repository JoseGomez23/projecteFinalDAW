from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UsuarioGrupo, GrupFamiliar, FavoriteProducts, ShoppingCartList, history as History, MercadoLivreCategory
from django.shortcuts import get_object_or_404
import requests
from django.http import JsonResponse
import uuid
from django.utils import timezone
import json
from django.conf import settings
import os
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dotenv import load_dotenv

from django.utils.http import url_has_allowed_host_and_scheme
import unicodedata
# Create your views here.




def index(request):
    return render(request, "index.html")

def recolectar_productos(request):
    
    url = "https://tienda.mercadona.es/api/categories/"
    response = requests.get(url)
    
   
    fecha_actualizacion = None
    try:
        with open(os.path.join(settings.BASE_DIR, 'static', 'products.json'), 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            fecha_actualizacion = json_data.get("fecha_actualizacion")
    except (FileNotFoundError, json.JSONDecodeError):
        fecha_actualizacion = None

    if fecha_actualizacion < datetime.now().strftime("%Y-%m-%d %H:%M:%S") or not fecha_actualizacion:
        if response.status_code == 200:
            data = response.json()
            subcategorias = []

            for categoria_principal in data.get("results", []):
                subcategorias.extend(categoria_principal.get("categories", []))
                

            #print(subcategorias)  # o haz lo que quieras con ellas
        else:
            subcategorias = []
            print("Error al obtener las categorías")
        
        
        productos = []

        for categoria in subcategorias:
            categoria_id = categoria.get("id")
            print(f"Consultando subcategoría {categoria_id}")
            
            url2 = f"https://tienda.mercadona.es/api/categories/{categoria_id}"
            response2 = requests.get(url2)

            if response2.status_code == 200:
                data2 = response2.json()
                subcategorias2 = data2.get("categories", [])

                for subcat in subcategorias2:
                    productos_en_subcat = subcat.get("products", [])
                    for producto in productos_en_subcat:
                        producto_info = {
                            "id": producto.get("id"),
                            "name": producto.get("display_name"),
                            "price": producto.get("price_instructions", {}).get("unit_price"),
                            "old_price": producto.get("price_instructions", {}).get("previous_unit_price"),
                            "image": producto.get("thumbnail")
                        }
                        productos.append(producto_info)
            else:
                print(f"Error en subcategoría {categoria_id}")



        #print(productos)
                    
        next_update = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        data_to_save = {
            "fecha_actualizacion": next_update.strftime("%Y-%m-%d %H:%M:%S"),
            "productos": productos
        }

        static_path = os.path.join(settings.BASE_DIR, 'static', 'products.json')

        with open(static_path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    url = "https://tienda.mercadona.es/api/categories/"
    response = requests.get(url)
    
    title = "Categories"

    if response.status_code == 200:
        data = response.json() 
        categorias = data.get("results", [])  
    else:
        categorias = []
    
    user = request.user
    group = []
    
    if user.is_authenticated:    
        userGroups = UsuarioGrupo.getGroups(request.user)
        group = [userGroup.group for userGroup in userGroups]
    
    urlMercadoLivre = request.build_absolute_uri()
    urlMercadoLivre = urlMercadoLivre.split("indexLogat/")[0]

    return render(request, "indexLogat.html", {"categories": categorias, "title": title, "groups": group, "urlMercadoLivre": urlMercadoLivre})


def searchProducts(request, search_query, group_id=""):

    static_path = os.path.join(settings.BASE_DIR, 'static', 'products.json')
    try:
        with open(static_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            productos = data.get("productos", [])
    except (FileNotFoundError, json.JSONDecodeError):
        productos = []

    def normalize(text):
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8').lower()

    search_normalized = normalize(search_query)
    user = request.user
    resultados = [

        producto for producto in productos
        if search_normalized in normalize(producto.get("name", ""))
    ]
    
    print(group_id)
    
    if request.user.is_authenticated and group_id:
        
        favorites = FavoriteProducts.getFavorites(request.user, group_id=group_id)
        shopingList = ShoppingCartList.getShoppingList(request.user, group_id=group_id)
        qnty = ShoppingCartList.getQty(request.user, group_id=group_id)
    elif request.user.is_authenticated:
        favorites = FavoriteProducts.getFavorites(request.user, group_id=None)
        shopingList = ShoppingCartList.getShoppingList(request.user, group_id=None)
        qnty = ShoppingCartList.getQty(request.user, group_id=None)
    else:
        favorites = []
        shopingList = []
        qnty = []
        
    if len(search_query) <= 2:
        resultados = []
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            "resultados": resultados,
            "user": user.username if user.is_authenticated else None,
            "favorites": list(favorites) if favorites else [],
            "shopingList": list(shopingList) if shopingList else [],
            "qnty": list(qnty) if qnty else []
        }, safe=False)

    return render(request, "indexLogat.html", {
        "search_query": search_query,
        "resultados": resultados,
        #"user": user
    })
    
def categories(request):
    
    url = "https://tienda.mercadona.es/api/categories/"
    response = requests.get(url)
    
    title = "Categories"

    if response.status_code == 200:
        data = response.json() 
        categorias = data.get("results", [])  
    else:
        categorias = []

    url1 = request.build_absolute_uri()
    
    url = url1.split("indexLogat/")[0]
        
    return render(request, "indexLogat.html", {"categories": categorias, "title": title, "url": url})

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


def categoriesMercadoLivre(request, group_id=""):
    
    category_id = request.GET.get("value", "") 
    
    print(category_id)
    
    user = request.user
    
    upd = timezone.now() + timedelta(days=1)
    
    mercado_livre_category = MercadoLivreCategory.getProductCategory(category_id)
    if mercado_livre_category:
        upd = mercado_livre_category.next_update
        
    print(upd)
    print(timezone.now())
    if user.is_authenticated:
        qnty = ShoppingCartList.getQty(user, group_id=None)
        favorites = FavoriteProducts.getFavorites(user, group_id=None)
        shopingList = ShoppingCartList.getShoppingList(user, group_id=None)
    else:
        qnty = []
        favorites = []
        shopingList = []
    
    if upd < timezone.now():
        
        load_dotenv()
        
        url = f"https://mercado-libre7.p.rapidapi.com/listings_for_category?category_url=https://lista.mercadolivre.com.br{category_id}&sort_by=relevance&page_num=1"

        headers = {
            "x-rapidapi-key": os.getenv("x-rapidapi-key"),
            "x-rapidapi-host": "mercado-libre7.p.rapidapi.com"
        }
        
        response = requests.get(url , headers=headers)
        
        products = []
        if response.status_code == 200:
            raw_products = response.json()
            for item in raw_products['data']:
                price = float(item.get('price', 0))
                realPrice = price * 0.16

                product, created = MercadoLivreCategory.getOrCreateProducts(
                    item.get('id'),
                    item.get('title'),
                    realPrice,
                    category_id
                )

                if not created:
                    product.price = round(realPrice, 2)
                    product.next_update = datetime.now() + timedelta(days=1)
                    product.save()
            
            products = MercadoLivreCategory.getProductsByCategory(category_id)
            
            print(products)
                    
            return render(request, "productsLidl.html", {"products": products, "title": "Products", "qnty": qnty, "favorites": favorites, "shopingList": shopingList})

        else:
            return render(request, "productsLidl.html", {"error": "Error al obtener productos de Mercado Livre"})
        
    else:
        
        products = MercadoLivreCategory.getProductsByCategory(category_id)
        
        if not products.exists():
            return render(request, "productsLidl.html", {"error": "No hay productos disponibles"})
    
   
    return render(request, "productsLidl.html", {"products": products, "title": "Products", "qnty": qnty, "favorites": favorites, "shopingList": shopingList})


def addProductToListMercadoLivre(request, product_id):

    if request.method == "POST":
        product = MercadoLivreCategory.getProduct(product_id)
        
        list_item, created = ShoppingCartList.getOrCreateProduct(
            user=request.user,
            group_id=None,
            product_id=product.id,
            name=product.title,
            image=None,
            price=product.price,
            old_price=None,
            quantity=1,
            supermarket=1
        )
        
        if not created:
            if list_item.quantity < 99:
                list_item.quantity += 1
                list_item.save()
            else:
                return JsonResponse({"message": "Maximum quantity reached"})
            
        return JsonResponse({"message": "Añadido al carrito" if created else "Cantidad incrementada en el carrito", "quantity": list_item.quantity})

        
def addFavoriteMercadoLivre(request, product_id):
    
    if request.method == "POST":
        product = MercadoLivreCategory.getProduct(product_id)
        
        favorite, created = FavoriteProducts.getOrCreateProduct(
            user=request.user,
            group_id=None,
            product_id=product.id,
            name=product.title,
            image=None,
            price=product.price,
            old_price=None
        )
        
        return JsonResponse({"message": "Añadido a favoritos" if created else "Ya estaba en favoritoss"})
    else:
        return JsonResponse({"error": "Metode no permés"}, status=405)
    
    
def removeFavoriteMercadoLivre(request, product_id):
    
    if request.method == "POST":
        try:
            favorite = FavoriteProducts.getFavoriteProduct(request.user, None, product_id)
            favorite.delete()
            return JsonResponse({"message": "Eliminat de favorits"})
        except FavoriteProducts.DoesNotExist:
            return JsonResponse({"error": "El producte no estava a favorits"}, status=404)
    return JsonResponse({"error": "Métode no permés"}, status=405)
            

def products(request, categoria_id, group_id=""):
    
    url = f"https://tienda.mercadona.es/api/categories/{categoria_id}"
    response = requests.get(url)
    products = []
    subcategory_id = None

    if response.status_code == 200:
        data = response.json()
        try:
            for subcategoria in data.get("categories", []):
                for product in subcategoria.get("products", []):
                    if product.get("published", False):
                        products.append(product)
            if products:
                first_product = products[0]
                subcategories = first_product.get("categories", [])
                if subcategories:
                    subcategory_id = subcategories[0].get("id")
        except:
            products = []
            subcategory_id = None
            
                
    favorites = []
    shopingList = []
    qnty = []
    group = []
    
    items_per_page = 40

   
    paginator = Paginator(products, items_per_page)

    
    page = request.GET.get("page", 1)

    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    if not group_id:
        if request.user.is_authenticated:
            userGroups = UsuarioGrupo.getGroups(request.user)
            group = [userGroup.group for userGroup in userGroups]
            favorites = FavoriteProducts.getFavorites(request.user, group_id=None)
            shopingList = ShoppingCartList.getShoppingList(request.user, group_id=None)
            qnty = ShoppingCartList.getQty(request.user, group_id=None)
            context = {
                "products": products_page,
                "favorites": favorites,
                "shopingList": shopingList,
                "qnty": qnty,
                "groups": group,
                "categoria_id": categoria_id,
                "subcategory_id": subcategory_id,
            }
        else:
            context = {
                "products": products_page,
                "categoria_id": categoria_id,
                "subcategory_id": subcategory_id,
            }
    else:
       
        if request.user.is_authenticated:
            group = UsuarioGrupo.getGroup(group_id)
            group = [group]
            favorites = FavoriteProducts.getFavorites(request.user, group_id=group_id)
            shopingList = ShoppingCartList.getShoppingList(request.user, group_id=group_id)
            qnty = ShoppingCartList.getQty(request.user, group_id=group_id)
            context = {
                "products": products_page,
                "favorites": favorites,
                "shopingList": shopingList,
                "qnty": qnty,
                "groups": group,
                "categoria_id": categoria_id,
                "subcategory_id": subcategory_id,
            }

    return render(request, "products.html", context)
    

    

@login_required
def groups(request):
    user_groups = UsuarioGrupo.getGroups(request.user)
    
    groups_with_members = []
    for user_group in user_groups:
        group = user_group.group
        members = UsuarioGrupo.getGroupUsers(group)
        groups_with_members.append({
            'group': group,
            'members': [member.user for member in members]
        })
    
    return render(request, 'grups.html', {'groups_with_members': groups_with_members})

@login_required
def leaveGroup(request, group_id):
    try:
        userGroup = UsuarioGrupo.getUserGroup(request.user, group_id)
        
        if not userGroup:
            return redirect('groups')
        
        group = userGroup.group
        userGroup.delete()
        
        if not UsuarioGrupo.objects.filter(group=group).exists():
            group.delete()

        return redirect('groups') 

    except UsuarioGrupo.DoesNotExist:
        return redirect('groups')  

def acceptInvite(request, group_id, invite_token):
    if not request.user.is_authenticated:
        return render(request, 'acceptInvite.html', {'error': 'Tienes que iniciar sesión para aceptar la invitación al grupo.'})

    group = get_object_or_404(GrupFamiliar, id=group_id)


    if group.invite_token != invite_token:
        return render(request, 'acceptInvite.html', {'error': 'El token de invitacion no es valido!'})

    if UsuarioGrupo.userInGroup(request.user, group):
        return render(request, 'acceptInvite.html', {'error': 'Ya eres miembro de este grupo!'})

    UsuarioGrupo.addUser(request.user, group)

    return render(request, 'acceptInvite.html', {'message': 'Se te ha añadido al grupo correctamente!'})

@login_required
def addFavorite(request, product_id, group_id=""):
    
    if request.method == "POST":
        
        url = f"https://tienda.mercadona.es/api/products/{product_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
        else:
            return JsonResponse({"error": "Producte no trobat"}, status=404)
            
        name = data.get("display_name", "")
        price = data.get("unit_price", 0)
        old_price = data.get("price_instructions.previous_unit_price", 0)
        image = data.get("thumbnail", "")
        
        #print(name)
        #print(image)
        
        price_info = data.get("price_instructions", {})
        price = price_info.get("unit_price", 0)
        old_price = price_info.get("previous_unit_price", 0)
        
        #print(price)
        #print(old_price)
        
        if not group_id:
            favorite, created = FavoriteProducts.getOrCreateProduct(
                user=request.user,
                group_id=None,
                product_id=product_id,
                name=name,
                image=image,
                price=price,
                old_price=old_price
            )
            return JsonResponse({"message": "Añadido a favoritos" if created else "Ya estaba en favoritos"})

        else:
            group_id = GrupFamiliar.getGroup(group_id)
            favorite, created = FavoriteProducts.getOrCreateProduct(
                user=request.user,
                group_id=group_id,
                product_id=product_id,
                name=name,
                image=image,
                price=price,
                old_price=old_price
            )
            return JsonResponse({"message": "Añadido a favoritos" if created else "Ya estaba en favoritos"})
        
    
    

@login_required
def showFavorites(request, group_id=""):
    
   
    
    if group_id:
        favorites = FavoriteProducts.getAllFavorites(None, group_id=group_id)
        shopingList = ShoppingCartList.getShoppingList(None, group_id=group_id)
        qnty = ShoppingCartList.getQty(None, group_id=group_id)
    else:
        favorites = FavoriteProducts.getAllFavorites(request.user, group_id=None)
        shopingList = ShoppingCartList.getShoppingList(request.user, group_id=None)
        qnty = ShoppingCartList.getQty(request.user, group_id=None)
        
    

    products = [
        {
            "id": favorite.product_id,
            "name": favorite.name,
            "price": favorite.price,
            "old_price": favorite.old_price,
            "image": favorite.image
        }
        for favorite in favorites
    ]

    # PAGINACIÓN
    items_per_page = 20
    paginator = Paginator(products, items_per_page)
    page = request.GET.get("page", 1)

    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    userGroups = UsuarioGrupo.getGroups(request.user)
    group = [userGroup.group for userGroup in userGroups]
    
    print(group_id)
    if group_id and group_id != "user":
        userIsInGroup = UsuarioGrupo.userInGroup(request.user, group_id)
        if not userIsInGroup:
            return render(request, "favorites.html", {"error": "No puedes ver los favoritos de otros grupos", "groups": group})
    
    
    

    return render(request, "favorites.html", {
        "products": products_page,
        "shopingList": shopingList,
        "qnty": qnty,
        "groups": group
    })


@login_required
def removeFavorites(request, product_id, group_id=""):
        
    if request.method == "POST":
        if not group_id:
            try:
                if not group_id:
                    favorite = FavoriteProducts.getFavoriteProduct(request.user, None, product_id)
                    favorite.delete()
                    
                else:
                    group = GrupFamiliar.getGroup(group_id)
                    favorite = FavoriteProducts.getFavoriteProduct(request.user, group, product_id)
                    favorite.delete()  
            
                return JsonResponse({"message": "Eliminado de favoritos"})
            except FavoriteProducts.DoesNotExist:
                return JsonResponse({"error": "El producte no estava a favorits"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@login_required
def addProductToList(request, product_id, group_id=None):
    if request.method == "POST":
        url = f"https://tienda.mercadona.es/api/products/{product_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
        
        name = data.get("display_name", "")
        price_info = data.get("price_instructions", {})
        price = price_info.get("unit_price", 0)
        old_price = price_info.get("previous_unit_price", 0)
        image = data.get("thumbnail", "")

        group = None
        if group_id:
            group = GrupFamiliar.getGroup(group_id)
            
        

        list_item, created = ShoppingCartList.getOrCreateProduct(
            user=request.user,
            group_id=group,
            product_id=product_id,
            name=name,
            image=image,
            price=price,
            old_price=old_price,
            quantity=1,
            supermarket=0
        )
        
        print(list_item)
        print(created)
        if not created:
            if list_item.quantity < 99:
                list_item.quantity += 1
                list_item.save()
            else:
                return JsonResponse({"message": "Maximum quantity reached"})

        return JsonResponse({"message": "Añadido al carrito" if created else "Cantidad incrementada en el carrito", "quantity": list_item.quantity})
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    
@login_required
def addOneProduct(request, product_id, group_id=""):
    try:
        if request.method == "POST":
            
            shoppingCartItem = ""
            
            if not group_id:
                shoppingCartItem = ShoppingCartList.getProduct(request.user, group_id=None, product_id=product_id)
            else:
                shoppingCartItem = ShoppingCartList.getProduct(None, group_id, product_id=product_id)
                
            if shoppingCartItem.quantity < 99:
                shoppingCartItem.quantity
                shoppingCartItem.quantity += 1
                shoppingCartItem.save()
                return JsonResponse({"quantity": shoppingCartItem.quantity})
            else:
                return JsonResponse({"message": "Maximum quantity reached"})
        else:
            return JsonResponse({"error": "Invalid request method"}, status=400)
    except ShoppingCartList.DoesNotExist:
        return JsonResponse({"error": "Product not found in shopping cart"}, status=404)
    
@login_required
def removeOneProduct(request, product_id, group_id=""):
    try:
        if request.method == "POST":
            
            shopping_cart_item = ""
            
            if not group_id or group_id == 1:
                shopping_cart_item = ShoppingCartList.getProduct(request.user, group_id=None, product_id=product_id)

            else:
                
                if not GrupFamiliar.objects.filter(id=group_id).exists():
                    return JsonResponse({"error": "Group does not exist"}, status=404)
                if not UsuarioGrupo.objects.filter(user=request.user, group_id=group_id).exists():
                    return JsonResponse({"error": "You are not a member of this group"}, status=403)
                
                shopping_cart_item = ShoppingCartList.getProduct(None, group_id, product_id)
            
            if shopping_cart_item.quantity > 1 and group_id != 1: 
                shopping_cart_item.quantity -= 1
                shopping_cart_item.save()
                return JsonResponse({"quantity": shopping_cart_item.quantity})
            elif shopping_cart_item.quantity > 1 and group_id == 1:
                shopping_cart_item.quantity -= 1
                shopping_cart_item.save()
                return JsonResponse({"quantity": shopping_cart_item.quantity})
            elif shopping_cart_item.quantity == 1 and group_id == 1:
                shopping_cart_item.delete()
                return JsonResponse({"message": "Product removed from cart"})
            else:
                return JsonResponse({"message": "Product removed from cart"})
        else:
            return JsonResponse({"error": "Invalid request method"}, status=400)
    except ShoppingCartList.DoesNotExist:
        return JsonResponse({"error": "Product not found in shopping cart"}, status=404)

@login_required
def removeProductFromList(request, product_id, group_id=""):
    if request.method == "POST":
        try:
            
            shopping_cart_item = ""
            
            if not group_id:
                shopping_cart_item = ShoppingCartList.getProduct(request.user, group_id=None, product_id=product_id)
            else:
                shopping_cart_item = ShoppingCartList.getProduct(None, group_id, product_id=product_id)
            
            shopping_cart_item.delete()
            return JsonResponse({"message": "Product removed from cart"})
        except ShoppingCartList.DoesNotExist:
            return JsonResponse({"error": "Product not found in shopping cart"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
    

@login_required
def shoppingCartList(request, group_id=""):
    
    if request.method == "GET":
        
        if group_id:

            if not UsuarioGrupo.userInGroup(request.user, group_id):
                return render (request, "shoppingCart.html", {"error": "No puedes ver la lista de otros grupos"}, status=403)
            shoppingCart = ShoppingCartList.getAllShoppingList(None, group_id=group_id)
            groupVar = GrupFamiliar.getGroup(group_id)
        else:
            shoppingCart = ShoppingCartList.getAllShoppingList(request.user, group_id=None)
            groupVar = "user"
            
        totalPrice = sum(item.price * item.quantity for item in shoppingCart)
        
        userGroups = UsuarioGrupo.getGroups(request.user)
        group = [userGroup.group for userGroup in userGroups]
        
        return render(request, "shoppingCart.html", {"shoppingCart": shoppingCart, "totalPrice": totalPrice, "groups": group, "groupVar": groupVar, "group_id": group_id})

@login_required
def history(request, group_id=None):
    if request.method == "GET":
        
        cart_items = []
        
        if group_id and group_id != "user":
            group = GrupFamiliar.getGroup(group_id)
            history_items = History.getHistory(None, group_id=group)
            cart_items = ShoppingCartList.getAllShoppingList(None, group_id=group)
        else:
            history_items = History.getHistory(request.user, group_id=None)
            cart_items = ShoppingCartList.getAllShoppingList(request.user, group_id=None)

        #cart_items = ShoppingCartList.objects.filter(user=request.user, group_id=group_id if group_id != "user" else None)
        cart_item_ids = list(cart_items.values_list("product_id", flat=True))

        user_groups = UsuarioGrupo.getGroups(request.user)
        groups = [user_group.group for user_group in user_groups]

        return render(request, "history.html", {
            "history": history_items,
            "cartItems": cart_item_ids,
            "groups": groups
        })

@login_required
def addFromHistory(request, product_id, ticket_id): #Hay que ver como lo refactorizo
    if request.method == "POST":
        
        history_ticket = History.objects.filter(user=request.user, ticket_id=ticket_id).first()
        if not history_ticket:
            return JsonResponse({"error": "Historial no encontrado"}, status=404)
        
        history_products = history_ticket.products or []
        product_data_from_history = next(
            (product for product in history_products if str(product.get("product_id")) == str(product_id)),
            None
        )

        if not product_data_from_history:
            return JsonResponse({"error": "Producto no encontrado en el historial"}, status=404)
    
        quantity = product_data_from_history.get("quantity", 1)
        
        url = f"https://tienda.mercadona.es/api/products/{product_id}"
        response = requests.get(url)
        if response.status_code != 200:
            return JsonResponse({"error": "No se pudo obtener el producto desde la API"}, status=404)

        product_data_api = response.json()

        
        name = product_data_api.get("display_name", "")
        price = product_data_api.get("price_instructions", {}).get("unit_price", 0)
        old_price = product_data_api.get("price_instructions", {}).get("previous_unit_price", 0)
        image = product_data_api.get("thumbnail", "")

        
        ShoppingCartList.objects.get_or_create(
            user=request.user,
            product_id=product_id,
            defaults={
                "name": name,
                "image": image,
                "price": price,
                "old_price": old_price,
                "quantity": quantity  
            }
        )

        return JsonResponse({"message": "Producto añadido al carrito desde el historial", "product": product_data_api})
    
    return JsonResponse({"error": "Método de solicitud no válido"}, status=400)


@login_required
def removeChecked(request, group_id=""):
    if request.method == "POST":
        
        print(group_id)
        
        if group_id == "user":
            group = None
        else:
            group = GrupFamiliar.getGroupByName(group_id)
            group_id_def = group.id
            
        selected_ids = request.POST.getlist("checkbox")
        
        #print(group_id_def)
        print(selected_ids)
        #print(group_id)
    
        redirect_url = None
        
        if group is None:
            redirect_url = "/shoppingCartList/"
        else:
            redirect_url = "/shoppingCartList/" + str(group_id_def) + "/"

        if selected_ids:
            if group is None:
                
                selected_items = ShoppingCartList.getCheckedProducts(
                    request.user,
                    selected_ids,
                    group_id=None
                )
            else:
                
                selected_items = ShoppingCartList.getCheckedProducts(
                    None,
                    selected_ids,
                    group_id=group
                )
                
                
            if selected_items.exists():
                
                new_ticket_id = f"TICKET-{uuid.uuid4().hex[:8]}"

                products_list = [
                    {
                        "product_id": item.product_id,
                        "name": item.name,
                        "price": float(item.price),
                        "old_price": float(item.old_price) if item.old_price else None,
                        "image": item.image,
                        "quantity": item.quantity
                    }
                    for item in selected_items
                ]
                
                History.createHistory(
                    user=request.user,
                    group_id=group,
                    ticket_id=new_ticket_id,
                    products_list=products_list
                )

                selected_items.delete()
            else:
                redirect(redirect_url)
                
                

        return redirect(redirect_url) 

    #return redirect(redirect_url)  


def productInfo(request, product_id, group_id=""):
    
    url = f"https://tienda.mercadona.es/api/products/{product_id}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        return render(request, "productInfo.html", {"error": "Producto no encontrado"})
        
    price_info = data.get("price_instructions", {})
    details = data.get("details", {})
    
    subcategories = data.get("categories", [])[0].get("categories", [])[0].get("id")
    
    #print(subcategories)
    
    product = {
        "id": product_id,
        "name": data.get("display_name", ""),
        "price": price_info.get("unit_price", 0),
        "old_price": price_info.get("previous_unit_price", 0),
        "image": data.get("thumbnail", ""),
        "brand": details.get("brand", ""),
        "origin": details.get("origin", ""),
        "usage_instructions": details.get("usage_instructions", "")
    }
    
    print(group_id)
    
    if request.user.is_authenticated:
        productDB = ShoppingCartList.getProduct(request.user, group_id=None, product_id=product_id)
        
        if productDB:
            productQty = productDB.quantity
        else:
            productQty = ""     
    else:
        productQty = ""
    
    
    return render(request, "productInfo.html", {"product": product, "productDB": productQty, "subcategory_id": subcategories})

def productInfoMercadoLivre(request, product_id):
    
    product = MercadoLivreCategory.getProduct(product_id)
    
    if request.user.is_authenticated:
        productDB = ShoppingCartList.getProduct(request.user, group_id=None, product_id=product_id)
        
        if productDB.exists():
            productQty = productDB.quantity
        else:
            productQty = ""
    else:
        productQty = ""
    
    return render(request, "productInfoMercadoLivre.html", {"product": product, "productDB": productQty})

def showMap(request):
    return render(request, "map2.html")

def refreshFavorites(request):
    if request.method == "POST":
        
        url = "https://tienda.mercadona.es/api/products/"
        
        if request.user.is_authenticated:
            favorites = FavoriteProducts.getFavorites(request.user, group_id=None)
            
            
            for product_id in favorites:
                product_url = f"{url}{product_id}"
                response = requests.get(product_url)
                if response.status_code == 200:
                    product_data = response.json()
                    FavoriteProducts.objects.filter(product_id=product_id).update(
                        name=product_data.get("display_name", ""),
                        price=product_data.get("price_instructions", {}).get("unit_price", 0),
                        old_price=product_data.get("price_instructions", {}).get("previous_unit_price", 0),
                        image=product_data.get("thumbnail", "")
                    )
                    
            return redirect("favorites")
            
        else:
            return redirect("login")
    
