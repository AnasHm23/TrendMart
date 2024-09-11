from django.shortcuts import render, redirect
from .models import Product, ProductImages, Category, Vendor
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
    product_images = ProductImages.objects.filter(product=product)
    related_products = Product.objects.filter(category=product.category).exclude(product_id=product.product_id)
  
    context = {
        'product': product,
        'related_products': related_products,
        'product_images': product_images,
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
    

def search_view(request):
    query = request.GET.get("q")
    product = None
    related_products = None
    
    if query:
        product = Product.objects.filter(title__icontains=query).first()
        
        if product:
            product_images = ProductImages.objects.filter(product=product)
            related_products = Product.objects.filter(category=product.category).exclude(product_id=product.product_id)
            messages.success(request, "here is the product you looking for")
        else:
            messages.warning(request, 'we could not find the product you looking for')
            return redirect('core:index')    
    
    context = {
        'product': product,
        'related_products': related_products,
        'product_images': product_images,
    }
    return render(request, 'core/product-details.html', context)

def filter_view(request):
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    
    products = Product.objects.all()
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
        
    if not products:
        messages.warning(request, "No products found for your the chosen range of price")
        return redirect('core:index')
    
    messages.success(request, 'Products have been successfully filtered!')
    context = {
        'products': products,
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, 'core/index.html', context)
