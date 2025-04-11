from django.shortcuts import render
from .forms import addProductApi

# Create your views here.
def addProduct(request):
    
    if request.method == 'POST':
        form = addProductApi(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data and save the product
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            
            # Here you would typically save the product to the database
            # For example:
            # Product.objects.create(name=name, description=description, price=price, image=image)
            
            return render(request, 'success.html', {'name': name})
    return render(request, 'add_product.html', {'form': addProductApi()})