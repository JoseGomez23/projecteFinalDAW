import uuid
from django.shortcuts import render, redirect
from django.urls import reverse
from projecteFinalDAW import settings
from .forms import Login, Register, AddUserToGroup, CreateGroup
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from app.models import UsuarioGrupo, GrupFamiliar

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
        return render(request, 'addGroupMember.html', {'form': AddUserToGroup(), 'groups': groups})
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
            invite_token = str(uuid.uuid4())
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
def createGroup(request):
    
    if request.method == 'GET':
        try:
            userGroup = UsuarioGrupo.objects.get(user=request.user)
            group = userGroup.group
            members = group.members.all()
        except UsuarioGrupo.DoesNotExist:
            group = None
            members = None

        return render(request, 'createGroup.html', {'form': CreateGroup(), 'group': group, 'members': members})
    else:
        
        if request.POST['name'] == '':
            return render(request, 'createGroup.html', {
            'form': CreateGroup(),
            'error': 'Has d\'omplir tots els camps'
            })
        
        try:
            group = GrupFamiliar.objects.create(name=request.POST['name'])
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