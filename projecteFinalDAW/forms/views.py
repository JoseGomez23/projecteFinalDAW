import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from projecteFinalDAW import settings
from .forms import Login, Register, AddUserToGroup, CreateGroup, QrCode
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import base64
import aspose.barcode as barcode
from .utils import generate_qr_code
from app.models import UsuarioGrupo, GrupFamiliar
import os
from app.models import GrupFamiliar
import re

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
                
                _login(request, user)
                next_url = request.GET.get('next', 'indexLogat')
                return redirect(next_url)
            
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
        
        # Guardar la imagen temporalmente
        with open('temp_qr_image.jpg', 'wb') as temp_file:
            for chunk in qr_image.chunks():
                temp_file.write(chunk)
        
        # Leer el código QR desde la imagen temporal
        reader = barcode.barcoderecognition.BarCodeReader('temp_qr_image.jpg')
        recognized_results = reader.read_bar_codes()
        
        # Eliminar la imagen temporal después de procesarla
        os.remove('temp_qr_image.jpg')
        
        result = ""
        # Mostrar resultados
        # Remove unused variable
        for result in recognized_results:
            raw_text = result.code_text
            
            # Eliminar todo después de '/acceptInvite/9/'
            if '/acceptInvite/' in raw_text:
                raw_text = re.sub(r'(/acceptInvite/\d+/).*', r'\1', raw_text)

            # Buscar el ID con regex
            match = re.search(r'/acceptInvite/(\d+)', raw_text)
            if match:
                invite_token = GrupFamiliar.objects.get(id=match.group(1)).invite_token
                
                result = raw_text + invite_token
            else:
               
                result = "No s'ha pogut extraure informació del QR."
        
        
            print(raw_text)
        
            if result.startswith('http://127.0.0.1:8000/acceptInvite/'):
                print("bomba")
                return render(request, 'readQr.html', {'results': result, 'form': QrCode()})
            else:
                print("nobomba")
                return render(request, 'readQr.html', {'error': 'Aquest lector només accepta QR de la pròpia web.', 'form': QrCode()})
        
        
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
            

def logout(request):
    _logout(request)
    return redirect('groups')