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
    
    def getApiToken(username):
        try:
            token = ApiToken.objects.get(user__username=username)
            return token
        except ApiToken.DoesNotExist:
            return None
        
    def getApiTokenHeader(token):
        try:
            token = ApiToken.objects.get(token=token)
            return token
        except ApiToken.DoesNotExist:
            return None
        
    def createToken(user, token, exp_date):
        try:
            api_token = ApiToken.objects.create(user=user, token=token, exp_date=exp_date)
            return api_token
        except ApiToken.DoesNotExist:
            return None
    
class PasswordToken(models.Model):
    token = models.CharField(max_length=100, verbose_name="Token de contrasenya")
    exp_date = models.DateTimeField(verbose_name="Data d'expiració")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  

    unique_together = ('token', 'user')
    
    def __str__(self):
        return self.user.username + ' - ' + self.token
    
    def getPasswordToken(user):
        try:
            token = PasswordToken.objects.get(user=user)
            return token
        except PasswordToken.DoesNotExist:
            return None
        
    def checkPasswordToken(token):
        try:
            token = PasswordToken.objects.get(token=token)
            return token
        except PasswordToken.DoesNotExist:
            return None
        
    def createPasswordToken(user, token, exp_date):
        try:
            password_token = PasswordToken.objects.create(user=user, token=token, exp_date=exp_date)
            return password_token
        except PasswordToken.DoesNotExist:
            return None
    
    
def getUser(username):
    try:
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
        return None
    
def getUserByEmail(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        return None