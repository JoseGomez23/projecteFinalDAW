from django import forms

class addProductApi(forms.Form):
    name = forms.CharField(label="Nombre del producto", max_length=100)
    old_price = forms.DecimalField(label="Preu antic (Pot ser blanc)", max_digits=10, decimal_places=2, required=False)
    price = forms.DecimalField(label="Preu del producte", max_digits=10, decimal_places=2)
    image_url = forms.CharField(label="URL de la imatge", max_length=1000)