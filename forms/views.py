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
from app.models import UsuarioGrupo, GrupFamiliar, createUser, getUser, getUserByEmail
from user.models import ApiToken, PasswordToken
import os
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
                'error': 'Debes rellenar todos los campos'
            })
            
        password_regex = re.compile(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$'
        )

        existsUser = getUserByEmail(request.POST['email'])
        
        if not password_regex.match(request.POST['password']):
            return render(request, 'register.html', {
                'form': Register(),
                'error': 'La contraseña no cumple los requisitos de seguridad (mínimo 8 caracteres, una mayúscula, una minúscula y un número)'
            })
        
        if request.POST['password'] == request.POST['password2'] and not existsUser:
            
            try: 
                user = createUser(request.POST['username'], request.POST['email'], request.POST['password'])
                user.save()
                
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                
                _login(request, user)
                return redirect('indexLogat')
            
            except IntegrityError:
                return render(request, 'register.html',{
                'form': Register(),
                'error': 'El usuario ya existe'
            })
        else:
            if existsUser:
                return render(request, 'register.html', {'form': Register(),
                    'error': 'Ya existe un usuario con ese correo electrónico'})
            
            # Si las contraseñas no coinciden
        return render(request, 'register.html', {'form': Register(),
        'error': 'Las contraseñas no coinciden'})

def login(request):
    
    if request.method == 'GET':
        
        return render(request, 'login.html',  {'form': Login()})
    else:
        
        if request.POST['username'] == '' or request.POST['password'] == '':
            return render(request, 'login.html', {
                'form': Login(),
                'error': 'Debes rellenar todos los campos'
            })
            
        else:
            
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            
            if user is None:
            
                return render(request, 'login.html', {
                    
                    'form': Login(),
                    'error': 'Correo electrónico o contraseña incorrectos'
                })
            else:
                
                user = getUser(request.POST['username'])

                apiToken = ApiToken.getApiToken(request.POST['username'])
                
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
                
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                _login(request, user)

                next_url = request.GET.get('next', 'index')
                response = redirect(next_url)
                
                response['Authorization'] = f'{apiToken.token}'
                
                response.set_cookie(
                key='Authorization',
                value=f'{apiToken.token}',  
                httponly=True,  
                secure=True,  
                samesite='Lax',  
                expires=apiToken.exp_date 
    )

    return response
            
@login_required
def groups(request, group_id):
    
    
    user_groups = UsuarioGrupo.getGroups(request.user)
    groups = [user_group.group for user_group in user_groups]
    
    if request.method == 'GET':
        
        try:
            group = GrupFamiliar.getGroup(group_id)
            invite_token = group.invite_token
            invite_url = request.build_absolute_uri(reverse('acceptInvite', args=[group_id, invite_token]))

            buffer = generate_qr_code(invite_url)
            qrCode = base64.b64encode(buffer.getvalue()).decode()
            
            return render(request, 'addGroupMember.html', {'form': AddUserToGroup(), 'groups': groups, 'qrCode': qrCode})
        except:
            return render(request, 'addGroupMember.html', {
                'error': 'El grupo no existe',
                'groups': groups
            })
    else:
        try:
            user = getUser(request.POST['username'])
            if user is None:
                return render(request, 'addGroupMember.html', {
                    'form': AddUserToGroup(),
                    'error': 'El usuario no existe',
                    'groups': groups
                })
                
            email = user.email
        except User.DoesNotExist:
            return render(request, 'addGroupMember.html', {
                'form': AddUserToGroup(),
                'error': 'El usuario no existe',
                'groups': groups
            })

        try:
            group = GrupFamiliar.getGroup(group_id)
        except GrupFamiliar.DoesNotExist:
            return render(request, 'addGroupMember.html', {
                'form': AddUserToGroup(),
                'error': 'El grupo no existe',
                'groups': groups
            })
            
            
        userExists = UsuarioGrupo.userInGroup(user, group)
        print(userExists)
        
        if  userExists:
            return render(request, 'addGroupMember.html', {
                'form': AddUserToGroup(),
                'error': 'El usuario ya pertenece a este grupo',
                'groups': groups
            })
         
        

        if email:
            
            invite_token = GrupFamiliar.getGroup(group_id).invite_token
            invite_url = request.build_absolute_uri(reverse('acceptInvite', args=[group.id, invite_token]))

            send_mail(
                '¡Bienvenido al grupo!',
                f'Has sido invitado a unirte al grupo {group.name} (ID: {group.id}). '
                f'Haz clic en el siguiente enlace para aceptar la invitación: {invite_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return render(request, 'addGroupMember.html', {
                'form': AddUserToGroup(),
                'message': 'Correo enviado correctamente, avisa al usuario de tu invitación',
                'groups': groups
            })
        else:
            return render(request, 'addGroupMember.html', {
                'form': AddUserToGroup(),
                'error': 'El usuario no tiene un correo electrónico vinculado',
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
               
                result = "No se ha podido extraer información del QR."
    
        
            if result.startswith('https://projectefinaldaw-2.onrender.com/') or result.startswith('http://127.0.0.1:8000/'):
                
                return render(request, 'readQr.html', {'results': result, 'form': QrCode()})
            else:
                
                return render(request, 'readQr.html', {'error': 'Este lector solo acepta QR de la propia web.', 'form': QrCode()})
        
        
    else:

        return render(request, 'readQr.html', {'form': QrCode()})

    
    return render(request, 'readQr.html', {'error': 'No se ha podido procesar la solicitud.', 'form': QrCode()})

@login_required
def createGroup(request):
    
    if request.method == 'GET':

        return render(request, 'createGroup.html', {'form': CreateGroup()})
    else:
        
        if request.POST['name'] == '':
            return render(request, 'createGroup.html', {
            'form': CreateGroup(),
            'error': 'Debes rellenar todos los campos'
            })
        
        try:
            group = GrupFamiliar.createGroup(request.POST['name'], str(uuid.uuid4()))
            userGroup = UsuarioGrupo.addUser(request.user, group)
            userGroup.save()
            return redirect('groups')
        except IntegrityError:
            return render(request, 'createGroup.html', {
            'form': CreateGroup(),
            'error': 'Ya existe un grupo con ese nombre'
            })

@login_required  
def addProductApi(request):
        
    if request.method == 'POST':
        
        name = request.POST['name']
        old_price = request.POST['old_price']
        price = request.POST['price']
        image_url = request.POST['image_url']
        print(image_url)
        
        exists = ApiProducts.getProduct(name=name, price=price)
        
        if exists:
            return render(request, 'addProductApi.html', {'error': "Este producto ya existe", 'form': apiForms.addProductApi()})
        
        if not old_price:
            old_price = None
        
        ApiProducts.createProduct(name=name, old_price=old_price, price=price, image=image_url)
        
        return render(request, 'addProductApi.html', {'name': "Producto añadido correctamente"})
    return render(request, 'addProductApi.html', {'form': apiForms.addProductApi()})


def sendEmail(request):

    if request.method == 'POST':
        
        email = request.POST['email']
        
        if email == "":
            return render(request, 'resetEmailPwd.html', {
                'form': ResetEmailPwd(),
                'error': 'Añade un correo electrónico'
            })
        
        try:
            user = getUserByEmail(email)
            token = str(uuid.uuid4())
            exp_date = datetime.now() + timedelta(hours=1)
            
            pwdToken = PasswordToken.getPasswordToken(user)
            
            if pwdToken:
                
                password_token = PasswordToken.objects.get(user=user)
                password_token.token = token
                password_token.exp_date = exp_date
                password_token.save()
            else:
                if user:
                    PasswordToken.createPasswordToken(user, token, exp_date)
                else:
                    return render(request, 'resetEmailPwd.html', {
                        'form': ResetEmailPwd(),
                        'error': 'No existe ningún usuario con ese correo electrónico'
                    })
            
            reset_url = request.build_absolute_uri(reverse('resetPassword', args=[token]))
            
            send_mail(
                'Restablecimiento de contraseña',
                f'Haz clic aquí para restablecer tu contraseña (1h para hacer el cambio a partir de este correo): <a href="{reset_url}">Haz clic aquí</a>',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=f'Haz clic aquí para restablecer tu contraseña (1h para hacer el cambio a partir de este correo): <a href="{reset_url}">Haz clic aquí</a>',
            )
            
            return render(request, 'resetEmailPwd.html', {
                'form': ResetEmailPwd(),
                'success': 'Se ha enviado un correo electrónico con las instrucciones para restablecer la contraseña'
            })
        
        except User.DoesNotExist:
            return render(request, 'resetEmailPwd.html', {
                'form': ResetEmailPwd(),
                'error': 'No existe ningún usuario con ese correo electrónico'
            })
    
    else:
        return render(request, 'resetEmailPwd.html', {'form': ResetEmailPwd()})
            
def resetPassword(request, token):
    
    if request.method == 'GET':
        
        try:
            password_token = PasswordToken.checkPasswordToken(token=token)
            
            if password_token.exp_date < datetime.now(password_token.exp_date.tzinfo):
                return render(request, 'resetPassword.html', {
                    'form': ResetPassword(),
                    'error': 'El token ha caducado'
                })
            
            return render(request, 'resetPassword.html', {'form': ResetPassword()})
        
        except PasswordToken.DoesNotExist:
            return render(request, 'resetPassword.html', {
                'form': ResetPassword(),
                'error': 'El token no existe'
            })
    
    else:
        
        if request.POST['password'] == request.POST['password2']:
            
            password_regex = re.compile(
                r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$'
            )
            if not password_regex.match(request.POST['password']):
                return render(request, 'resetPassword.html', {
                    'form': ResetPassword(),
                    'error': 'La contraseña no cumple los requisitos de seguridad (mínimo 8 caracteres, una mayúscula, una minúscula, un número y un símbolo especial)'
                })
            
            try:
                password_token = PasswordToken.checkPasswordToken(token=token)
                
                user = password_token.user
                
                user.set_password(request.POST['password'])
                user.save()
                
                password_token.delete()
                
                return redirect('login')
            
            except PasswordToken.DoesNotExist:
                return render(request, 'resetPassword.html', {
                    'form': ResetPassword(),
                    'error': 'El token no existe'
                })
        else:
            return render(request, 'resetPassword.html', {
                'form': ResetPassword(),
                'error': 'Las contraseñas no coinciden'
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
                'error': 'Debes rellenar todos los campos'
            })
        
        if request.POST['password'] == request.POST['password2']:
            
            if user.check_password(request.POST['oldPassword']):
                
                password_regex = re.compile(
                    r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$'
                )

                if not password_regex.match(request.POST['password']):
                    return render(request, 'manualResetPwd.html', {
                        'form': ResetManualPassword(),
                        'error': 'La contraseña no cumple los requisitos de seguridad (mínimo 8 caracteres, una mayúscula, una minúscula, un número y un símbolo especial)'
                    })

                user.set_password(request.POST['password'])
                user.save()
                
                _login(request, user)
                
                return redirect('indexLogat')
            
            else:
                
                return render(request, 'manualResetPwd.html', {
                    'form': ResetManualPassword(),
                    'error': 'La contraseña actual no es correcta'
                })
        else:
            
            return render(request, 'manualResetPwd.html', {
                'form': ResetManualPassword(),
                'error': 'Las contraseñas no coinciden'
            })

def logout(request):
        
    _logout(request)
    return redirect('login')