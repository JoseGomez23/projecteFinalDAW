from django.contrib import admin
from .models import ApiToken, PasswordToken

# Register your models here.
admin.site.register(ApiToken)
admin.site.register(PasswordToken)