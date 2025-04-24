from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ApiToken(models.Model):
    token = models.CharField(max_length=100, verbose_name="Token d'API")
    exp_date = models.DateTimeField(verbose_name="Data d'expiració")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  

    unique_together = ('token', 'user')
    
    def __str__(self):
        return self.user.username + ' - ' + self.token