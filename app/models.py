from django.db import models
from django.contrib.auth.models import User


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
        
    def getUsers(group):
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
    
class MercadoLivreCategory(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_id = models.CharField(max_length=255)
    next_update = models.DateTimeField(null=True, blank=True)
    
    
    def __str__(self):
        return self.id + " - " + self.title
    

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