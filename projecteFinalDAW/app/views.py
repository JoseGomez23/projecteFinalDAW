from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UsuarioGrupo, GrupFamiliar, FavoriteProducts, ShoppingCartList, history as History
from django.shortcuts import get_object_or_404
import requests
from django.http import JsonResponse
import uuid
import json
from datetime import datetime, timedelta
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

def products(request, categoria_id, group_id=""):
    
    if not group_id:
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
        shopingList = []
        
        userGroups = UsuarioGrupo.objects.filter(user=request.user)
        group = [userGroup.group for userGroup in userGroups]
        
        #print(group)
        
        
        if request.user.is_authenticated:    
            favorites = FavoriteProducts.objects.filter(user=request.user, group_id=None).values_list("product_id", flat=True)
            shopingList = ShoppingCartList.objects.filter(user=request.user, group_id=None).values_list("product_id", flat=True)
            qnty = ShoppingCartList.objects.filter(user=request.user, group_id=None).values_list("product_id", "quantity")
            

        return render(request, "products.html", {
            "products": products,
            "favorites": favorites,
            "shopingList": shopingList,
            "qnty": qnty,
            "groups": group,
            "categoria_id": categoria_id
        })
    
    else:
        
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
        shopingList = []
        
        group = UsuarioGrupo.objects.filter(group_id=group_id)
        
        
        #print(group)
        
        #print(group_id)
        
        
        if request.user.is_authenticated:    
            favorites = FavoriteProducts.objects.filter(group_id=group_id).values_list("product_id", flat=True)
            shopingList = ShoppingCartList.objects.filter(group_id=group_id).values_list("product_id", flat=True)
            qnty = ShoppingCartList.objects.filter(group_id=group_id).values_list("product_id", "quantity")
            

        return render(request, "products.html", {
            "products": products,
            "favorites": favorites,
            "shopingList": shopingList,
            "qnty": qnty,
            "groups": group,
            "categoria_id": categoria_id
        })
    

    

@login_required
def groups(request):
    user_groups = UsuarioGrupo.objects.filter(user=request.user).select_related('group')
    
    groups_with_members = []
    for user_group in user_groups:
        group = user_group.group
        members = UsuarioGrupo.objects.filter(group=group).select_related('user')
        groups_with_members.append({
            'group': group,
            'members': [member.user for member in members]
        })
    
    return render(request, 'grups.html', {'groups_with_members': groups_with_members})

@login_required
def leaveGroup(request, group_id):
    try:
        userGroup = UsuarioGrupo.objects.get(user=request.user, group_id=group_id)
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

    # Check if the invite token matches
    if group.invite_token != invite_token:
        return render(request, 'acceptInvite.html', {'error': 'El token d\'invitació no és vàlid!'})

    if UsuarioGrupo.objects.filter(user=request.user, group=group).exists():
        return render(request, 'acceptInvite.html', {'error': 'Ja ets membre d\'aquest grup!'})

    UsuarioGrupo.objects.create(user=request.user, group=group)

    return render(request, 'acceptInvite.html', {'message': 'Has estat afegit al grup correctament!'})

@login_required
def addFavorite(request, product_id, group_id=""):
    
    if request.method == "POST":
        if not group_id:
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
            
            #print(price)
            #print(old_price)
            
            if request.method == "POST":
                favorite, created = FavoriteProducts.objects.get_or_create(user=request.user, product_id=product_id, name=name, image=image, price=price, old_price=old_price)
                return JsonResponse({"message": "Añadido a favoritos" if created else "Ya estaba en favoritos"})
            return JsonResponse({"error": "Método no permitido"}, status=405)
        else:
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
            
            #print(price)
            #print(old_price)
            
            group = GrupFamiliar.objects.get(id=int(group_id))
            
            if request.method == "POST":
                favorite, created = FavoriteProducts.objects.get_or_create(user=request.user, group_id=group, product_id=product_id, name=name, image=image, price=price, old_price=old_price)
                return JsonResponse({"message": "Añadido a favoritos" if created else "Ya estaba en favoritos"})
    
    

@login_required
def showFavorites(request, group_id=""):
    if group_id:
        favorites = FavoriteProducts.objects.filter(group_id=group_id)
        shopingList = ShoppingCartList.objects.filter(group_id=group_id).values_list("product_id", flat=True)
        qnty = ShoppingCartList.objects.filter(group_id=group_id).values_list("product_id", "quantity")
    else:
        favorites = FavoriteProducts.objects.filter(user=request.user, group_id=None)
        shopingList = ShoppingCartList.objects.filter(user=request.user).values_list("product_id", flat=True)
        qnty = ShoppingCartList.objects.filter(user=request.user).values_list("product_id", "quantity")

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

    userGroups = UsuarioGrupo.objects.filter(user=request.user)
    group = [userGroup.group for userGroup in userGroups]

    return render(request, "favorites.html", {"products": products, "shopingList": shopingList, "qnty": qnty, "groups": group})

@login_required
def removeFavorites(request, product_id, group_id=""):
        
    if request.method == "POST":
        if not group_id:
            try:
                favorite = FavoriteProducts.objects.get(user=request.user, product_id=product_id, group_id=None)
                favorite.delete()
                return JsonResponse({"message": "Eliminado de favoritos"})
            except FavoriteProducts.DoesNotExist:
                return JsonResponse({"error": "El producto no estaba en favoritos"}, status=404)
        else:
            try:
                favorite = FavoriteProducts.objects.get(user=request.user, group_id=group_id, product_id=product_id)
                favorite.delete()
                return JsonResponse({"message": "Eliminado de favoritos"})
            except FavoriteProducts.DoesNotExist:
                return JsonResponse({"error": "El producto no estaba en favoritos"}, status=404)
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
            group = GrupFamiliar.objects.get(id=int(group_id))

        list_item, created = ShoppingCartList.objects.get_or_create(
            user=request.user,
            group_id=group,
            product_id=product_id,
            defaults={"name": name, "image": image, "price": price, "old_price": old_price, "quantity": 1}
        )
        
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
                shoppingCartItem = ShoppingCartList.objects.get(user=request.user, product_id=product_id, group_id=None)
            else:
                shoppingCartItem = ShoppingCartList.objects.get(group_id=group_id, product_id=product_id)
                
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
            
            if not group_id:
                shopping_cart_item = ShoppingCartList.objects.get(user=request.user, product_id=product_id, group_id=None)
            else:
                
                if not GrupFamiliar.objects.filter(id=group_id).exists():
                    return JsonResponse({"error": "Group does not exist"}, status=404)
                if not UsuarioGrupo.objects.filter(user=request.user, group_id=group_id).exists():
                    return JsonResponse({"error": "You are not a member of this group"}, status=403)
                
                shopping_cart_item = ShoppingCartList.objects.get(group_id=group_id, product_id=product_id)
            
            if shopping_cart_item.quantity > 1: 
                shopping_cart_item.quantity -= 1
                shopping_cart_item.save()
                return JsonResponse({"quantity": shopping_cart_item.quantity})
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
                shopping_cart_item = ShoppingCartList.objects.get(user=request.user, product_id=product_id, group_id=None)
            else:
                shopping_cart_item = ShoppingCartList.objects.get(group_id=group_id, product_id=product_id)
            
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

            if not UsuarioGrupo.objects.filter(user=request.user, group_id=group_id).exists():
                return render (request, "shoppingCart.html", {"error": "No pots veure llistes d'altres grups"}, status=403)
            shoppingCart = ShoppingCartList.objects.filter(group_id=group_id)
            groupVar = GrupFamiliar.objects.get(id=int(group_id))
        else:
            shoppingCart = ShoppingCartList.objects.filter(user=request.user, group_id=None)
            groupVar = "user"
            
        totalPrice = sum(item.price * item.quantity for item in shoppingCart)
        
        userGroups = UsuarioGrupo.objects.filter(user=request.user)
        group = [userGroup.group for userGroup in userGroups]
        
        return render(request, "shoppingCart.html", {"shoppingCart": shoppingCart, "totalPrice": totalPrice, "groups": group, "groupVar": groupVar, "group_id": group_id})

@login_required
def history(request, group_id=None):
    if request.method == "GET":
        if group_id and group_id != "user":
            group = GrupFamiliar.objects.get(id=group_id)
            history_items = History.objects.filter(user=request.user, group_id=group)
        else:
            history_items = History.objects.filter(user=request.user, group_id=None)

        cart_items = ShoppingCartList.objects.filter(user=request.user, group_id=group_id if group_id != "user" else None)
        cart_item_ids = list(cart_items.values_list("product_id", flat=True))

        user_groups = UsuarioGrupo.objects.filter(user=request.user).select_related('group')
        groups = [user_group.group for user_group in user_groups]

        return render(request, "history.html", {
            "history": history_items,
            "cartItems": cart_item_ids,
            "groups": groups
        })

@login_required
def addFromHistory(request, product_id, ticket_id):
    if request.method == "POST":
        
        historyTicket = History.objects.filter(user=request.user, ticket_id=ticket_id).first()
        
        historyTicketProducts = historyTicket.products if historyTicket else []
         
        separated_products = []
        for product in historyTicketProducts:
            separated_products.append(product.get("product_id"))
            
        print(separated_products)
        print(product_id)
        
        product_id = str(product_id)
        
        separated_products_str = ", ".join(separated_products)
        
        if product_id in separated_products_str:
            product_data = next((product for product in historyTicketProducts if product.get("product_id") == product_id), None)
            if product_data:
                ShoppingCartList.objects.get_or_create(
                    user=request.user,
                    product_id=product_id,
                    defaults={
                    "name": product_data.get("name", ""),
                    "image": product_data.get("image", ""),
                    "price": product_data.get("price", 0),
                    "old_price": product_data.get("old_price", 0),
                    "quantity": 1
                    }
                    )
                
                return JsonResponse({"message": "Product added to cart", "product": product_data})
            else:
                return JsonResponse({"error": "Product not found in history"}, status=404)
        
        else:
            return JsonResponse({"error": "Product not found in history"}, status=404)
            
    return JsonResponse({"error": "Invalid request method"}, status=400)



@login_required
def removeChecked(request, group_id=""):
    if request.method == "POST":
        
        #print(group_id)
        
        if group_id == "user":
            group = None
        else:
            group = GrupFamiliar.objects.get(name=group_id)
            group_id_def = group.id
            
        selected_ids = request.POST.getlist("checkbox")
        
        print(group_id_def)
        #print(selected_ids)
        #print(group_id)
    
        redirect_url = None

        if selected_ids:
            if group is None:
                selected_items = ShoppingCartList.objects.filter(user=request.user, product_id__in=selected_ids, group_id=None)
                
            else:
                selected_items = ShoppingCartList.objects.filter(product_id__in=selected_ids, group_id=group)
                
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

                History.objects.create(
                    user=request.user,
                    group_id=group,
                    ticket_id=new_ticket_id,
                    products=products_list
                )

                selected_items.delete()
                
                

        return redirect("/shoppingCartList/" + str(group_id_def) + "/") 

    return redirect("redirect_url")  # Redirect if the method is not POST
