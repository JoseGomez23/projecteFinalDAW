from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import Config
from django.shortcuts import render
from .forms import Config
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
        
        print(username)
        print(email)
        
        print(request.user.username)
        print(request.user.email)
        
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
    


