from django import forms

class addProductApi(forms.Form):
    name = forms.CharField(label="Nombre del producto", max_length=100)
    old_price = forms.DecimalField(label="Precio antiguo (Se puede dejar en blanco)", max_digits=10, decimal_places=2, required=False)
    price = forms.DecimalField(label="Precio del producto", max_digits=10, decimal_places=2)
    image_url = forms.CharField(label="Url del producto", max_length=1000)