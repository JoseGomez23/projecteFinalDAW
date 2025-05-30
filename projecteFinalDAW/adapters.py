# projecteFinalDAW/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model, login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta
from app.models import getUserByEmail
from user.models import ApiToken
import uuid
User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Si un usuario con el mismo email ya existe, lo asociamos y lo iniciamos sesión
        """
        email = sociallogin.account.extra_data.get('email')
        if email:
            user = getUserByEmail(email)
            if user:
                sociallogin.connect(request, user)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                
                apiToken = ApiToken.getApiToken(user)
                
                if apiToken:
                    
                    apiToken.token = str(uuid.uuid4())
                    apiToken.exp_date = datetime.now() + timedelta(hours=1)
                    apiToken.save()
                
                else:
                    
                    token_str = str(uuid.uuid4())
                    exp_date = datetime.now() + timedelta(hours=1)
                    
                    ApiToken.createToken(user, token=token_str, exp_date=exp_date)
                
                auth_login(request, user)
                raise ImmediateHttpResponse(HttpResponseRedirect(reverse('index')))
    
    def is_auto_signup_allowed(self, request, sociallogin):
        return True
