from django import forms

class Config(forms.Form):
    
    username = forms.CharField(
        label="Nombre de usuario", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'configInputs'})
    )
    email = forms.EmailField(
        label="Correo electronico",
        widget=forms.EmailInput(attrs={'class': 'configInputs'})
    )
    
    
