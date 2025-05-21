from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import Config
from .forms import Config
from .models import getUser
from app.models import FavoriteProducts, GrupFamiliar, UsuarioGrupo
# Create your views here.

@login_required
def configuration(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            initial_data = {
                "username": request.user.username,
                "email": request.user.email
            }
            
            form = Config(initial=initial_data)  
            return render(request, "userConfiguration.html", {"form": form})
        else:
            return render(request, "userConfiguration.html", {"form": form, "error": "Has de logar-te per poder accedir a aquesta pàgina"})
    elif request.method == 'POST':
        
        initial_data = {}
        username = request.POST['username']
        email = request.POST['email']
        
        #print(username)
        #print(email)
        
        #print(request.user.username)
        #print(request.user.email)
        
        if username != request.user.username or email != request.user.email:
            
            userExists = getUser(username)
            
            if not userExists:
                user = request.user
                user.username = username
                user.email = email
                user.save()
                form = Config(initial={"username": user.username, "email": user.email})
                return render(request, "userConfiguration.html", {"form": form, "message": "La configuración se ha actualizado correctamente"})
            else:
                form = Config(initial={"username": username, "email": email})
                return render(request, "userConfiguration.html", {"form": form, "error": "Ya existe un usuario con ese nombre de usuario"})
        else:
            form = Config(initial={"username": username, "email": email})
            return render(request, "userConfiguration.html", {"form": form, "error": "Debes cambiar algún campo para poder actualizar la configuración"})
    
@login_required
def deleteAccount(request):
    if request.method == 'GET':
        
        user = getUser(request.user.username)
        
        usuario_grupo = UsuarioGrupo.getGroups(user)
        group_name = None

        if usuario_grupo:
            groups = GrupFamiliar.objects.filter(id__in=UsuarioGrupo.objects.filter(user=request.user).values_list('group_id', flat=True))
            group_name = [group.name for group in groups]
            
            #print(group_name)

        qtFavProducts = FavoriteProducts.objects.filter(user=request.user).count()
        
        return render(request, "deleteUser.html", {"group": group_name, "qtFavProducts": qtFavProducts})
    elif request.method == 'POST':
        
        user = getUser(request.user.username)
        
        userGroups = UsuarioGrupo.getGroups(user)

        for userGroup in userGroups:
            group = userGroup.group
            userGroup.delete()
            
            if not UsuarioGrupo.hasUsers(group):
                group.delete()

        
        user = request.user
        user.delete()
        
        return redirect("index")
    else:
        return render(request, "userConfiguration.html", {"error": "Se ha producido un error al eliminar el usuario"})

