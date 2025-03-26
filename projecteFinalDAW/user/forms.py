from django import forms

class Config(forms.Form):
    
    username = forms.CharField(label="Nom de l'usuari", max_length=100)
    email = forms.EmailField(label="Correu electrònic")
    
    
