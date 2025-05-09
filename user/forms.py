from django import forms

class Config(forms.Form):
    
    username = forms.CharField(
        label="Nom de l'usuari", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'configInputs'})
    )
    email = forms.EmailField(
        label="Correu electrònic",
        widget=forms.EmailInput(attrs={'class': 'configInputs'})
    )
    
    
