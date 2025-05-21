from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


# Create your models here.
class GrupFamiliar(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    invite_token = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
    def createGroup(name, token):
        group = GrupFamiliar.objects.create(name=name, invite_token=token)
        return group
    
    def getGroup(id):
        try:
            group = GrupFamiliar.objects.get(id=id)
            return group
        except GrupFamiliar.DoesNotExist:
            return None
    
    def getGroupByName(name):
        try:
            group = GrupFamiliar.objects.get(name=name)
            return group
        except GrupFamiliar.DoesNotExist:
            return None

class UsuarioGrupo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    group = models.ForeignKey(GrupFamiliar, on_delete=models.CASCADE, related_name="members")  

    class Meta:
        unique_together = ('user', 'group')  

    def __str__(self):
        return self.group.name + ' - ' + self.user.username
    
    def getGroup(user):
        try:
            group = UsuarioGrupo.objects.get(user=user)
            return group.group
        except UsuarioGrupo.DoesNotExist:
            return None
        
    def getGroups(user):
        try:
            groups = UsuarioGrupo.objects.filter(user=user)
            return groups
        except UsuarioGrupo.DoesNotExist:
            return None
        
    def hasUsers(group):
        try:
            users = UsuarioGrupo.objects.filter(group=group).exists()
            return users
        except UsuarioGrupo.DoesNotExist:
            return None
        
    def userInGroup(user, group):
        try:
            user = UsuarioGrupo.objects.filter(user=user, group=group).exists()
            print(user)
            return True
        except UsuarioGrupo.DoesNotExist:
            return False
        
    def addUser(user, group):
        try:
            user = UsuarioGrupo.objects.create(user=user, group=group)
            return user
        except UsuarioGrupo.DoesNotExist:
            return user
        
    def getGroupUsers(group):
        try:
            users = UsuarioGrupo.objects.filter(group=group)
            return users
        except UsuarioGrupo.DoesNotExist:
            return None
        
    def getUserGroup(user, group_id):
        try:
            user = UsuarioGrupo.objects.get(user=user, group_id=group_id)
            return user.group
        except UsuarioGrupo.DoesNotExist:
            return None
    
    
class FavoriteProducts(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(GrupFamiliar, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    old_price = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    image = models.URLField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'product_id', 'group_id')  
        
    def __str__(self):
        return f"{self.user.username} - {self.product_id}"
    
    def getFavorites(user, group_id):
        try:
            
            if user is not None:
                favorites = FavoriteProducts.objects.filter(user=user, group_id=group_id).values_list("product_id", flat=True)
                return favorites
            else:
                favorites = FavoriteProducts.objects.filter(group_id=group_id).values_list("product_id", flat=True)
                return favorites
        except FavoriteProducts.DoesNotExist:
            return None
        
    def getOrCreateProduct(user, group_id,product_id, name, price, old_price, image):
        product, created = FavoriteProducts.objects.get_or_create(
            user=user,
            group_id=group_id,
            product_id=product_id,
            defaults={
                'name': name,
                'price': price,
                'old_price': old_price,
                'image': image
            }
        )
        return product, created
    
    def getFavoriteProduct(user, group_id, product_id):
        try:
            product = FavoriteProducts.objects.get(user=user, group_id=group_id ,product_id=product_id)
            return product
        except FavoriteProducts.DoesNotExist:
            return None
        
    def getAllFavorites(user, group_id):
        try:
            if user is not None:
                favorites = FavoriteProducts.objects.filter(user=user, group_id=group_id)
            else:
                favorites = FavoriteProducts.objects.filter(group_id=group_id)
            return favorites
        except FavoriteProducts.DoesNotExist:
            return None
    
    
    
    
class ShoppingCartList(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(GrupFamiliar, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    old_price = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    image = models.URLField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    supermarket = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'product_id', 'group_id')
        
    def __str__(self):
        return f"{self.user.username} - {self.name} - {self.quantity}"
    
    def getQty(user, group_id):
        try:
            if user is not None:
                qty = ShoppingCartList.objects.filter(user=user, group_id=group_id).values_list("product_id", "quantity")
                return qty
            else:
                qty = ShoppingCartList.objects.filter(group_id=group_id).values_list("product_id", "quantity")
                return qty
        except ShoppingCartList.DoesNotExist:
            return 0
        
    def getShoppingList(user, group_id):
        try:
            if user is not None:
                shopping_list = ShoppingCartList.objects.filter(user=user, group_id=group_id).values_list("product_id", flat=True)
                return shopping_list
            else:
                shopping_list = ShoppingCartList.objects.filter(group_id=group_id).values_list("product_id", flat=True)
                return shopping_list
        except ShoppingCartList.DoesNotExist:
            return None
        
    def getOrCreateProduct(user, group_id,product_id, name, price, old_price, image, quantity, supermarket):
        product, created = ShoppingCartList.objects.get_or_create(
            user=user,
            group_id= group_id,
            product_id=product_id,
            defaults={
                'name': name,
                'price': price,
                'old_price': old_price,
                'image': image,
                'quantity': quantity,
                'supermarket': supermarket
            }
        )
        if not created:
            product.quantity += quantity
            product.save()
        return product, created
    
    def getProduct(user, group_id, product_id):
        try:
            if user is not None:
                product = ShoppingCartList.objects.get(user=user, group_id=group_id ,product_id=product_id)
                return product
            else:
                product = ShoppingCartList.objects.get(group_id=group_id ,product_id=product_id)
                return product
        except ShoppingCartList.DoesNotExist:
            return None
    
    def getAllShoppingList(user, group_id):
        try:
            if user is not None:
                shopping_list = ShoppingCartList.objects.filter(user=user, group_id=group_id)
            else:
                shopping_list = ShoppingCartList.objects.filter(group_id=group_id)
            return shopping_list
        except ShoppingCartList.DoesNotExist:
            return None

    def getCheckedProducts(user, selected_ids, group_id):
        try:
            if user is not None:
                checked_products = ShoppingCartList.objects.filter(user=user, product_id__in=selected_ids, group_id=None)
                return checked_products
            else:
                checked_products = ShoppingCartList.objects.filter(product_id__in=selected_ids, group_id=group_id)
                return checked_products
        except ShoppingCartList.DoesNotExist:
            return None
        

class history(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(GrupFamiliar, on_delete=models.CASCADE, null=True, blank=True)
    ticket_id = models.CharField(max_length=255)
    products = models.JSONField(default=list) 
    date = models.DateTimeField(auto_now_add=True)

    def add_product(self, product):
        if not self.products:
            self.products = []
        
        
        for p in self.products:
            if p["product_id"] == product["product_id"]:
                p["quantity"] += product["quantity"]
                break
        else:
            self.products.append(product)

        self.save()

    def __str__(self):
        return f"Historial de {self.user.username} - Ticket {self.ticket_id}"
    
    def getHistory(user, group_id):
        try:
            if user is not None:
                list = history.objects.filter(user=user, group_id=group_id)
                return list
            else:
                list = history.objects.filter(group_id=group_id)
                return list
        except history.DoesNotExist:
            return None
    
    def createHistory(user, group_id, ticket_id, products_list):
        history.objects.create(
            user=user,
            group_id=group_id,
            ticket_id=ticket_id,
            products=products_list
        )
    
    
class MercadoLivreCategory(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_id = models.CharField(max_length=255)
    next_update = models.DateTimeField(null=True, blank=True)
    
    
    def __str__(self):
        return self.id + " - " + self.title
    
    def getProductCategory(id):
        try:
            category = MercadoLivreCategory.objects.filter(category_id=id).first()
            return category
        except MercadoLivreCategory.DoesNotExist:
            return None
        
    def getOrCreateProducts(id, title, price, category_id):
        product, created = MercadoLivreCategory.objects.get_or_create(
            id=id,
            defaults={
                'title': title,
                'price': round(price, 2),
                'category_id': category_id,
                'next_update': datetime.now() + timedelta(days=1)
            }
        )
        return product, created
    
    def getProduct(id):
        try:
            product = MercadoLivreCategory.objects.get(id=id)
            return product
        except MercadoLivreCategory.DoesNotExist:
            return None
    

def getUser(username):
    try:
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
        return None

def createUser(username, email, password):
    user = User.objects.create_user(username=username, password=password, email=email)
    return user

def getUserByEmail(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        return None