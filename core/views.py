from django.shortcuts import render
from .models import Product

# Create your views here.
def index(request):
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(price__lt=8, price__gt=3).order_by("-id")
    
    context = {
        'products': products
    }
    return render(request, 'core/index.html', context) 

def product_list(request):
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.all().order_by("-id")
    context = {
        'products': products
    }
    return render(request, 'core/product_list.html', context) 

