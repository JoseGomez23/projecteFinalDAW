from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import Config
from .forms import Config
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
            
            user = request.user
            user.username = username
            user.email = email
            user.save()
            form = Config(initial={"username": user.username, "email": user.email})
            return render(request, "userConfiguration.html", {"form": form, "message": "La configuració s'ha actualitzat correctament"})
        else:
            form = Config(initial={"username": username, "email": email})
            return render(request, "userConfiguration.html", {"form": form, "error": "Has de canviar algun camp per poder actualitzar la configuració"})
    
@login_required
def deleteAccount(request):
    if request.method == 'GET':
        
        usuario_grupo = UsuarioGrupo.objects.filter(user=request.user).first()
        group_name = None

        if usuario_grupo:
            groups = GrupFamiliar.objects.filter(id__in=UsuarioGrupo.objects.filter(user=request.user).values_list('group_id', flat=True))
            group_name = [group.name for group in groups]
            
            #print(group_name)

        qtFavProducts = FavoriteProducts.objects.filter(user=request.user).count()
        
        return render(request, "deleteUser.html", {"group": group_name, "qtFavProducts": qtFavProducts})
    elif request.method == 'POST':
        
        userGroup = UsuarioGrupo.objects.filter(user=request.user)
        
        #print(userGroup)
        
        if userGroup:
            group = userGroup.group
            userGroup.delete()
            
            if not UsuarioGrupo.objects.filter(group=group).exists():
                group.delete()
        
        user = request.user
        user.delete()
        
        return redirect("index")
    else:
        return render(request, "userConfiguration.html", {"error": "S'ha produït un error a l'hora d'eliminar l'usuari"})

