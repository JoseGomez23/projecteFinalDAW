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
        else:
            initial_data = {}

    form = Config(initial=initial_data)  
    return render(request, "userConfiguration.html", {"form": form})


