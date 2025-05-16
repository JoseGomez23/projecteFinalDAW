from django import forms

class Login(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=100)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
    
class Register(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=100)
    email = forms.CharField(label="Correo del usuario", max_length=100)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Repite la contraseña", widget=forms.PasswordInput())
    
class AddUserToGroup(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=100)
    
class CreateGroup(forms.Form):
    name = forms.CharField(label="Nombre del grupo", max_length=100)

class QrCode(forms.Form):
    image = forms.ImageField(label="Código QR", required=True)
    
class ResetEmailPwd(forms.Form):
    email = forms.CharField(label="Correo del usuario", max_length=100)
    
class ResetPassword(forms.Form):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Repite la contraseña", widget=forms.PasswordInput())
    
class ResetManualPassword(forms.Form):
    oldPassword = forms.CharField(label="Contraseña actual", widget=forms.PasswordInput())
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Repite la contraseña", widget=forms.PasswordInput())