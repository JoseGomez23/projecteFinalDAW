from django.utils import timezone
from django.shortcuts import render
from .forms import addProductApi
from .models import ApiProducts
from user.models import ApiToken
from django.http import JsonResponse
# Create your views here.

def getProducts(request):
    
    result = authHelper(request)
    
    if result != True:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    else:
        products = ApiProducts.objects.all()
        return JsonResponse({'products': list(products.values())})

def getProduct(request, name):
    
    result = authHelper(request)
    
    if result != True:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    else:
        try:
            products = ApiProducts.objects.filter(name__iregex=name)
            if products.exists():
                return JsonResponse({'products': list(products.values())})
            else:
                return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def getProductP(request, price):
    
    result = authHelper(request)
    
    if result != True:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    else:
        try:
            products = ApiProducts.objects.filter(price=price)
            if products.exists():
                return JsonResponse({'products': list(products.values())})
            else:
                return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)        

        
def getProductHigher(request, price):
        
    result = authHelper(request)
    
    if result != True:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    else:
        try:
            products = ApiProducts.objects.filter(price__gt=price)
            if products.exists():
                return JsonResponse({'products': list(products.values())})
            else:
                return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
def getProductPLower(request, price):
            
    result = authHelper(request)
    
    if result != True:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    else:
        try:
            products = ApiProducts.objects.filter(price__lt=price)
            if products.exists():
                return JsonResponse({'products': list(products.values())})
            else:
                return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
def getProductWithDiscount(request, boolean):
    
    result = authHelper(request)
    
    if result != True:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    else:
        try:
            
            boolean = str(boolean).capitalize()
            
            if boolean != "True":
                products = ApiProducts.objects.filter(old_price__gt=0)
            else:
                products = ApiProducts.objects.filter(old_price=None)
                
            if products.exists():
                return JsonResponse({'products': list(products.values())})
            else:
                return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
def authHelper(request):
    
    auth_header = request.headers.get('Authorization')  
    authorization_cookie = request.COOKIES.get('Authorization')

    
    if auth_header:
        print("Authorization header:", auth_header)
        
        token_obj = ApiToken.objects.filter(token=auth_header).first()
        
        if not token_obj:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        if token_obj.exp_date < timezone.now():
            return JsonResponse({
                'error': 'Token expired',
                'now': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                'expires_at': token_obj.exp_date.strftime("%Y-%m-%d %H:%M:%S")
            }, status=401)

        return True
    elif authorization_cookie:
        
        print("Authorization cookie:", authorization_cookie)
        
        token_obj = ApiToken.objects.filter(token=authorization_cookie).first()
        
        print("Token object:", token_obj)

        if not token_obj:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        if token_obj.exp_date < timezone.now():
            return JsonResponse({
                'error': 'Token expired',
                'now': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                'expires_at': token_obj.exp_date.strftime("%Y-%m-%d %H:%M:%S")
            }, status=401)

        return True    
