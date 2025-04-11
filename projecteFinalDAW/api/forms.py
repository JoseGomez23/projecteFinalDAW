from django import forms

class addProductApi(forms.Form):
    name = forms.CharField(label="Nom del producte", max_length=100)
    description = forms.CharField(label="Descripció del producte", max_length=1000)
    price = forms.DecimalField(label="Preu del producte", max_digits=10, decimal_places=2)
    image = forms.ImageField(label="Imatge del producte", required=False)