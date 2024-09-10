from django.shortcuts import render, redirect
from .models import Product, Category, Vendor
from django.contrib import messages


def index(request):
    return render(request, 'core/index.html') 

def product_list(request):
    products = Product.objects.all().order_by("-id")
    context = {
        'products': products
    }
    return render(request, 'core/product_list.html', context) 

def product_detail(request, pid):
    product = Product.objects.get(product_id=pid)
    related_products = Product.objects.filter(category=product.category).exclude(product_id=product.product_id)
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'core/product-details.html', context)

def category_products_list(request, cid):
    category = Category.objects.get(category_id=cid)
    
    if category is not None:
        products = Product.objects.filter(category=category)
        messages.success(request, f"here are all the products related to {category.title} category")
        context = {
            'category': category,
            'products': products,
        }
        return render(request, 'core/category-products-list.html', context)
    else:
        messages.error(request, "the category doesn't exist")
        return redirect("core:index")

def vendor_products_list(request, vid):
    vendor = Vendor.objects.get(vendor_id=vid)
    
    if vendor is not None:
        products = Product.objects.filter(vendor=vendor)
        messages.success(request, "here are all the products related to the chosen vendor")
        context = {
            'vendor': vendor,
            'products': products,
        }
        return render(request, "core/vendor-products.html", context)
    else:
        messages.error(request, "vendor doesn't exist")
        return redirect("core:index")