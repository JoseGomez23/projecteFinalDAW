# projecteFinalDAW/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model, login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.models import getUserByEmail

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
                auth_login(request, user)
                raise ImmediateHttpResponse(HttpResponseRedirect(reverse('index')))
            # Si el usuario no existe, dejamos que Allauth continúe el flujo normal de registro.
    
    def is_auto_signup_allowed(self, request, sociallogin):
        return True
