import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from projecteFinalDAW import settings
from .forms import Login, Register, AddUserToGroup, CreateGroup, QrCode, ResetEmailPwd, ResetPassword, ResetManualPassword
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import base64
import api.forms as apiForms
from api.models import ApiProducts
import aspose.barcode as barcode
from .utils import generate_qr_code
from app.models import UsuarioGrupo, GrupFamiliar
from user.models import ApiToken, PasswordToken
import os
from app.models import GrupFamiliar
import re
from datetime import datetime, timedelta

# Create your views here.
def register(request):
    
    if request.method == 'GET':
        
        return render(request, 'register.html',  {'form': Register()})
    else:
        
        if request.POST['username'] == '' or request.POST['email'] == '' or request.POST['password'] == '' or request.POST['password2'] == '':
            return render(request, 'register.html', {
                'form': Register(),
                'error': 'Has d\'omplir tots els camps'
            })
        
        if request.POST['password'] == request.POST['password2']:
            
            try: 
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'] ,password=request.POST['password'])
                user.save()
                _login(request, user)
                return redirect('indexLogat')
            
            except IntegrityError:
                return render(request, 'register.html',{
                'form': Register(),
                'error': 'L\'usuari ja existeix'
            })
        return render(request, 'register.html', {'form': Register(),
        'error': 'Les contrasenyes no coincideixen'})

def login(request):
    
    if request.method == 'GET':
        
        return render(request, 'login.html',  {'form': Login()})
    else:
        
        if request.POST['username'] == '' or request.POST['password'] == '':
            return render(request, 'login.html', {
                'form': Login(),
                'error': 'Has d\'omplir tots els camps'
            })
            
        else:
            
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            
            if user is None:
            
                return render(request, 'login.html', {
                    
                    'form': Login(),
                    'error': 'eMail o contrasenya incorrectes'
                })
            else:
                
                user = User.objects.get(username=request.POST['username'])

                apiToken = ApiToken.objects.filter(user=user).first()
                
                if apiToken:
                    apiToken.token = str(uuid.uuid4())
                    apiToken.exp_date = datetime.now() + timedelta(hours=1)
                    apiToken.save()
                    
                    
                else:
                    token_str = str(uuid.uuid4())
                    exp_date = datetime.now() + timedelta(hours=1)

                    apiToken = ApiToken.objects.create(
                        user=user,
                        token=token_str,
                        exp_date=exp_date
                    )
                
                _login(request, user)

                next_url = request.GET.get('next', 'indexLogat')
                response = redirect(next_url)
                
                response['Authorization'] = f'{apiToken.token}'
                
                response.set_cookie(
                key='Authorization',
                value=f'{apiToken.token}',  # Estilo típico de auth header
                httponly=True,  # Importante para seguridad
                secure=True,  # Solo HTTPS
                samesite='Lax',  # Puedes usar 'Strict' o 'None' si es necesario
                expires=apiToken.exp_date  # Expira cuando expire el token
    )

    return response
            
@login_required
def groups(request, group_id):
    user_groups = UsuarioGrupo.objects.filter(user=request.user)
    groups = [user_group.group for user_group in user_groups]
    
    

    if request.method == 'GET':
        
        group = GrupFamiliar.objects.get(id=group_id)
        invite_token = group.invite_token
        invite_url = request.build_absolute_uri(reverse('acceptInvite', args=[group_id, invite_token]))

        buffer = generate_qr_code(invite_url)
        qrCode = base64.b64encode(buffer.getvalue()).decode()
        
        return render(request, 'addGroupMember.html', {'form': AddUserToGroup(), 'groups': groups, 'qrCode': qrCode})
    else:
        try:
            user = User.objects.get(username=request.POST['username'])
            email = user.email
        except User.DoesNotExist:
            return render(request, 'addGroupMember.html', {
                'form': AddUserToGroup(),
                'error': 'L\'usuari no existeix',
                'groups': groups
            })

        try:
            group = GrupFamiliar.objects.get(id=group_id)
        except GrupFamiliar.DoesNotExist:
            return render(request, 'addGroupMember.html', {
                'form': AddUserToGroup(),
                'error': 'El grup no existeix',
                'groups': groups
            })

        if UsuarioGrupo.objects.filter(user=user, group=group).exists():
            return render(request, 'addGroupMember.html', {
                'form': AddUserToGroup(),
                'error': 'L\'usuari ja pertany a aquest grup',
                'groups': groups
            })

        if email:
            invite_token = GrupFamiliar.objects.get(id=group_id).invite_token
            invite_url = request.build_absolute_uri(reverse('acceptInvite', args=[group.id, invite_token]))

            send_mail(
                'Benvingut al grup!',
                f'Has estat convidat a unir-te al grup {group.name} (ID: {group.id}). '
                f'Fes clic al següent enllaç per acceptar la invitació: {invite_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return render(request, 'addGroupMember.html', {
                'form': AddUserToGroup(),
                'message': 'Correu enviat correctament, avisa a l\'usuari de la teva invitació',
                'groups': groups
            })
        else:
            return render(request, 'addGroupMember.html', {
                'form': AddUserToGroup(),
                'error': 'L\'usuari no té un correu electrònic vinculat',
                'groups': groups
            })
         
@login_required   
def qrReader(request):
    if request.method == 'POST' and request.FILES.get('image'):
        qr_image = request.FILES['image']
        
        with open('temp_qr_image.jpg', 'wb') as temp_file:
            for chunk in qr_image.chunks():
                temp_file.write(chunk)
        
        reader = barcode.barcoderecognition.BarCodeReader('temp_qr_image.jpg')
        recognized_results = reader.read_bar_codes()
        
        os.remove('temp_qr_image.jpg')
        
        result = ""
        
        for result in recognized_results:
            raw_text = result.code_text
            
            if '/acceptInvite/' in raw_text:
                raw_text = re.sub(r'(/acceptInvite/\d+/).*', r'\1', raw_text)

            match = re.search(r'/acceptInvite/(\d+)', raw_text)
            if match:
                invite_token = GrupFamiliar.objects.get(id=match.group(1)).invite_token
                
                result = raw_text + invite_token
            else:
               
                result = "No s'ha pogut extraure informació del QR."
        
        
            print(raw_text)
        
            if result.startswith('https://projectefinaldaw-2.onrender.com/acceptInvite/'):
                
                return render(request, 'readQr.html', {'results': result, 'form': QrCode()})
            else:
                
                return render(request, 'readQr.html', {'error': 'Aquest lector només accepta QR\'s de la pròpia web.', 'form': QrCode()})
        
        
    else:

        return render(request, 'readQr.html', {'form': QrCode()})

    
    return render(request, 'readQr.html', {'error': 'No s\'ha pogut processar la sol·licitud.', 'form': QrCode()})

@login_required
def createGroup(request):
    
    if request.method == 'GET':

        return render(request, 'createGroup.html', {'form': CreateGroup()})
    else:
        
        if request.POST['name'] == '':
            return render(request, 'createGroup.html', {
            'form': CreateGroup(),
            'error': 'Has d\'omplir tots els camps'
            })
        
        try:
            group = GrupFamiliar.objects.create(name=request.POST['name'], invite_token=str(uuid.uuid4()))
            userGroup = UsuarioGrupo.objects.create(user=request.user, group=group)
            userGroup.save()
            return redirect('groups')
        except IntegrityError:
            return render(request, 'createGroup.html', {
            'form': CreateGroup(),
            'error': 'Ja existeix un grup amb aquest nom'
            })
            
def addProductApi(request):
        
    if request.method == 'POST':
        
        name = request.POST['name']
        old_price = request.POST['old_price']
        price = request.POST['price']
        image_url = request.POST['image_url']
        
        exists = ApiProducts.objects.filter(name=name, price=price)
        
        if exists:
            return render(request, 'addProductApi.html', {'error': "Aquest producte ja existeix", 'form': apiForms.addProductApi()})
        
        if not old_price:
            old_price = None
        
        ApiProducts.objects.create(name=name, old_price=old_price, price=price, image_url=image_url)
        
        return render(request, 'addProductApi.html', {'name': name})
    return render(request, 'addProductApi.html', {'form': apiForms.addProductApi()})


def sendEmail(request):

    if request.method == 'POST':
        
        email = request.POST['email']
        
        if email == "":
            return render(request, 'resetEmailPwd.html', {
                'form': ResetEmailPwd(),
                'error': 'Afegeix un correu electrònic'
            })
        
        try:
            user = User.objects.get(email=email)
            token = str(uuid.uuid4())
            exp_date = datetime.now() + timedelta(hours=1)
            
            if PasswordToken.objects.filter(user=user).exists():
                password_token = PasswordToken.objects.get(user=user)
                password_token.token = token
                password_token.exp_date = exp_date
                password_token.save()
            
            PasswordToken.objects.create(user=user, token=token, exp_date=exp_date)
            
            reset_url = "http://127.0.1:8000/ resetPassword/" + token
            
            send_mail(
                'Restabliment de contrasenya',
                f'Fes clic aquí per restablir la teva contrasenya (1h per fer el canvi a partir d\'aquest correu): <a href="{reset_url}">Fes clic aquí</a>',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=f'Fes clic aquí per restablir la teva contrasenya (1h per fer el canvi a partir d\'aquest correu): <a href="{reset_url}">Fes clic aquí</a>',
            )
            
            return render(request, 'resetEmailPwd.html', {
                'form': ResetEmailPwd(),
                'message': 'S\'ha enviat un correu electrònic amb les instruccions per restablir la contrasenya'
            })
        
        except User.DoesNotExist:
            return render(request, 'resetEmailPwd.html', {
                'form': ResetEmailPwd(),
                'error': 'No existeix cap usuari amb aquest correu electrònic'
            })
    
    else:
        return render(request, 'resetEmailPwd.html', {'form': ResetEmailPwd()})
            
def resetPassword(request, token):
    
    if request.method == 'GET':
        
        try:
            password_token = PasswordToken.objects.get(token=token)
            
            print(password_token.exp_date)
            print(datetime.now())
            
            
            if password_token.exp_date < datetime.now(password_token.exp_date.tzinfo):
                return render(request, 'resetPassword.html', {
                    'form': ResetPassword(),
                    'error': 'El token ha caducat'
                })
            
            return render(request, 'resetPassword.html', {'form': ResetPassword()})
        
        except PasswordToken.DoesNotExist:
            return render(request, 'resetPassword.html', {
                'form': ResetPassword(),
                'error': 'El token no existeix'
            })
    
    else:
        
        if request.POST['password'] == request.POST['password2']:
            
            try:
                password_token = PasswordToken.objects.get(token=token)
                
                user = password_token.user
                
                user.set_password(request.POST['password'])
                user.save()
                
                password_token.delete()
                
                return redirect('login')
            
            except PasswordToken.DoesNotExist:
                return render(request, 'resetPassword.html', {
                    'form': ResetPassword(),
                    'error': 'El token no existeix'
                })
        else:
            return render(request, 'resetPassword.html', {
                'form': ResetPassword(),
                'error': 'Les contrasenyes no coincideixen'
            })

@login_required          
def manualResetPwd(request):
    
    if request.method == 'GET':
        
        return render(request, 'manualResetPwd.html', {'form': ResetManualPassword()})
    
    else:
        
        user = request.user
        
        if request.POST['oldPassword'] == '' or request.POST['password'] == '' or request.POST['password2'] == '':
            return render(request, 'manualResetPwd.html', {
                'form': ResetManualPassword(),
                'error': 'Has d\'omplir tots els camps'
            })
        
        if request.POST['password'] == request.POST['password2']:
            
            if user.check_password(request.POST['oldPassword']):
                
                password_regex = re.compile(
                    r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
                )

                if not password_regex.match(request.POST['password']):
                    return render(request, 'manualResetPwd.html', {
                        'form': ResetManualPassword(),
                        'error': 'La contrasenya no compleix els requisits de seguretat (mínim 8 caràcters, una majúscula, una minúscula, un número i un símbol especial)'
                    })

                user.set_password(request.POST['password'])
                user.save()
                
                _login(request, user)
                
                return redirect('indexLogat')
            
            else:
                
                return render(request, 'manualResetPwd.html', {
                    'form': ResetManualPassword(),
                    'error': 'La contrasenya actual no és correcta'
                })
        else:
            
            return render(request, 'manualResetPwd.html', {
                'form': ResetManualPassword(),
                'error': 'Les contrasenyes no coincideixen'
            })

def logout(request):
        
    _logout(request)
    return redirect('login')