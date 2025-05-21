from django.db import models

# Create your models here.
class ApiProducts(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom del producte")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Preu antic del producte")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preu del producte")
    image_url = models.CharField(max_length=2000,blank=True, null=True, verbose_name="Imatge del producte")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'image_url', 'price') 
        
    def getProducts():
        try:
            products = ApiProducts.objects.all()
            return products
        except ApiProducts.DoesNotExist:
            return None
        
    def getProduct(name, price):
        try:
            product = ApiProducts.objects.filter(name=name, price=price)
            return product
        except ApiProducts.DoesNotExist:
            return None
        
    def createProduct(name, old_price, price, image_url):
        try:
            product =  ApiProducts.objects.create(name=name, old_price=old_price, price=price, image_url=image_url)
            return product
        except ApiProducts.DoesNotExist:
            return None
        
    def getProductsByName(name):
        try:
            products = ApiProducts.objects.filter(name__iregex=name)
            return products
        except ApiProducts.DoesNotExist:
            return None
        
    def getProductsByPrice(price):
        try:
            products = ApiProducts.objects.filter(price=price)
            return products
        except ApiProducts.DoesNotExist:
            return None
        
    def getProductsByHigherPrice(price):
        try:
            products = ApiProducts.objects.filter(price__gt=price)
            return products
        except ApiProducts.DoesNotExist:
            return None
        
    def getProductsByLowerPrice(price):
        try:
            products = ApiProducts.objects.filter(price__lt=price)
            return products
        except ApiProducts.DoesNotExist:
            return None
        
    def getProductsWithDiscount():
        try:
            products = ApiProducts.objects.filter(old_price__gt=0)
            return products
        except ApiProducts.DoesNotExist:
            return None
        
    def getProductsWithouthDiscount():
        try:
            products = ApiProducts.objects.filter(old_price__isnull=True)
            return products
        except ApiProducts.DoesNotExist:
            return None