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