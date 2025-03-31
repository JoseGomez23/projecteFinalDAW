from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class GrupFamiliar(models.Model):
    name = models.CharField(max_length=100, unique=True)  

    def __str__(self):
        return self.name

class UsuarioGrupo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    group = models.ForeignKey(GrupFamiliar, on_delete=models.CASCADE, related_name="members")  

    def __str__(self):
        return self.group.name + ' - ' + self.user.username
    
    
class FavoriteProducts(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    product_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    old_price = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    image = models.URLField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'product_id')  
        
    def __str__(self):
        return f"{self.user.username} - {self.product_id}"
    
    
class ShoppingCartList(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    old_price = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    image = models.URLField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('user', 'product_id')
        
    def __str__(self):
        return f"{self.user.username} - {self.name} - {self.quantity}"
    
class history(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    old_price = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    image = models.URLField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    
    
