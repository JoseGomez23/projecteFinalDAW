from django import forms

class Login(forms.Form):
    username = forms.CharField(label="Nom de l'usuari", max_length=100)
    password = forms.CharField(label="Contrasenya", widget=forms.PasswordInput())
    
class Register(forms.Form):
    username = forms.CharField(label="Nom d'usuari", max_length=100)
    email = forms.CharField(label="Correu de l'usuari", max_length=100)
    password = forms.CharField(label="Contrasenya", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Repeteix la contrasenya", widget=forms.PasswordInput())
    
class AddUserToGroup(forms.Form):
    username = forms.CharField(label="Nom d'usuari", max_length=100)
    
class CreateGroup(forms.Form):
    name = forms.CharField(label="Nom del grup", max_length=100)

class QrCode(forms.Form):
    image = forms.ImageField(label="QR Code", required=True)
    
class ResetEmailPwd(forms.Form):
    email = forms.CharField(label="Correu de l'usuari", max_length=100)
    
class ResetPassword(forms.Form):
    password = forms.CharField(label="Contrasenya", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Repeteix la contrasenya", widget=forms.PasswordInput())
    
class ResetManualPassword(forms.Form):
    oldPassword = forms.CharField(label="Contrasenya actual", widget=forms.PasswordInput())
    password = forms.CharField(label="Contrasenya", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Repeteix la contrasenya", widget=forms.PasswordInput())