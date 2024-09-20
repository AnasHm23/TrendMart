from django.shortcuts import render, redirect
from .models import Product, ProductImages, Category, Vendor, Order, OrderItem
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils import timezone


def index(request):
    products = Product.objects.all().order_by("-id")
    top_selling = Product.objects.all().order_by("-id")[9:]
    recently_added = Product.objects.all().order_by("-id")[:3]    
    trendig_products = Product.objects.all().order_by("-id")[3:6]
    top_rated = Product.objects.all().order_by("-id")[6:9]
    
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    
    try:
        product_paginated = paginator.page(page)
    except PageNotAnInteger:
        product_paginated = paginator.page(1)
    except EmptyPage:
        product_paginated = paginator.page(paginator.num_pages)
     
    context = {
        'products': product_paginated,
        'top_selling': top_selling,
        'recently_added': recently_added,
        'trendig_products': trendig_products,
        'top_rated': top_rated,
    }
    return render(request, 'core/index.html', context)

def product_list(request):
    products = Product.objects.all().order_by("-id")
    
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    
    try:
        products_paginated = paginator.page(page)
    except PageNotAnInteger:
        products_paginated = paginator.page(1)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)
    
    context = {
        'products': products_paginated
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
        products = Product.objects.filter(category=category).order_by("-id")
    
        paginator = Paginator(products, 10)
        page = request.GET.get('page')
        
        try:
            products_paginated = paginator.page(page)
        except PageNotAnInteger:
            products_paginated = paginator.page(1)
        except EmptyPage:
            products_paginated = paginator.page(paginator.num_pages)
        messages.success(request, f"here are all the products related to {category.title} category")
        context = {
            'category': category,
            'products': products_paginated,
        }
        return render(request, 'core/category-products-list.html', context)
    else:
        messages.error(request, "the category doesn't exist")
        return redirect("core:index")

def vendor_products_list(request, vid):
    vendor = Vendor.objects.get(vendor_id=vid)
    
    if vendor is not None:
        products = Product.objects.filter(vendor=vendor).order_by("-id")
    
        paginator = Paginator(products, 10)
        page = request.GET.get('page')
        
        try:
            products_paginated = paginator.page(page)
        except PageNotAnInteger:
            products_paginated = paginator.page(1)
        except EmptyPage:
            products_paginated = paginator.page(paginator.num_pages)
        messages.success(request, "here are all the products related to the chosen vendor")
        context = {
            'vendor': vendor,
            'products': products_paginated,
        }
        return render(request, "core/vendor-products.html", context)
    else:
        messages.error(request, "vendor doesn't exist")
        return redirect("core:index")
    


def search_view(request):
    query = request.POST.get("q")
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
    min_price = request.POST.get("min_price")
    max_price = request.POST.get("max_price")
    
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

def cart_list(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            if item['price'] and item['qty']:
                try:
                    cart_total_amount += int(item['qty']) * float(item['price'])
                except ValueError:
                    continue
            else:
                continue
        
        return render(request, 'core/cart_list.html', {
            'cart_data': request.session['cart_data_obj'], 
            'totalcartitems': len(request.session['cart_data_obj']), 
            'cart_total_amount': cart_total_amount
        })
    else:
        messages.warning(request, "Your cart is empty")
        return redirect('core:index')


def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET.get('pid'),
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
            request.session.modified = True
    else:
        request.session['cart_data_obj']= cart_product
    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

def delete_from_cart(request):
    id = request.POST.get('id')
    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        if id in cart_data:
            del cart_data[id]
            request.session['cart_data_obj'] = cart_data
            
            request.session.modified = True

        for p_id, item in cart_data.items():
            cart_total_amount += int(item['qty']) * float(item['price'])

        if not cart_data:
            del request.session['cart_data_obj']
            context = {
                "data": {},
                'totalcartitems': 0,
                'cart_total_amount': 0,
            }
        else:
            context = {
                "data": cart_data,
                'totalcartitems': len(cart_data),
                'cart_total_amount': cart_total_amount,
            }
    else:
        context = {
            "data": {},
            'totalcartitems': 0,
            'cart_total_amount': 0,
        }

    return JsonResponse(context)

def update_cart(request):
    id = request.POST.get('id')
    qty = request.POST.get('qty')
    cart_total_amount = 0
    
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        
        if id in cart_data:
            cart_data[id]['qty'] = qty
            request.session['cart_data_obj'] = cart_data
            request.session.modified = True
        
        for p_id, item in cart_data.items():
            cart_total_amount += int(item['qty']) * float(item['price'])

        context = {
            "data": cart_data,
            'totalcartitems': len(cart_data),
            'cart_total_amount': cart_total_amount,
            'qty': qty,
        }
    else:
        context = {
            "data": {},
            'totalcartitems': 0,
            'cart_total_amount': 0,
        }

    return JsonResponse(context)

def clear_cart(request):
    if request.method == 'POST':
        if 'cart_data_obj' in request.session:
            del request.session['cart_data_obj']
            request.session.modified = True
        return JsonResponse({'message': 'Cart cleared successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def wishlist_view(request):
    if request.method == 'POST':
        wishlist_product = {}
        id = str(request.POST.get('id'))
        wishlist_product[id] = {
            'title': request.POST.get('title'),
            'price': request.POST.get('price'),
            'image': request.POST.get('image'),
            'pid': request.POST.get('pid'),
        }

        if 'wishlist_data_obj' in request.session:
            if id in request.session['wishlist_data_obj']:
                messages.warning(request, "The product is already in your Wishlist")
            else:
                wishlist_data = request.session['wishlist_data_obj']
                wishlist_data.update(wishlist_product)
                request.session['wishlist_data_obj'] = wishlist_data
                request.session.modified = True
        else:
            request.session['wishlist_data_obj'] = wishlist_product
            request.session.modified = True

        return JsonResponse({
            'data': request.session['wishlist_data_obj'],
        })
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def delete_from_wishlist(request):
    id = request.POST.get('id')

    if 'wishlist_data_obj' in request.session:
        wishlist_data = request.session['wishlist_data_obj']

        if id in wishlist_data:
            del wishlist_data[id]
            request.session['wishlist_data_obj'] = wishlist_data
            
            request.session.modified = True
            context = {
                'data': wishlist_data
            }
        else: 
            context = {
                "data": wishlist_data,
            }
    else:
        context = {
            "data": {},
        }

    return JsonResponse(context)

def checkout_view(request):
    return render(request, 'core/checkout.html')


def place_order(request):
    if request.method == 'POST':
        # Assuming that the cart data is stored in the session
        cart_data = request.session.get('cart_data_obj', {})
        if not cart_data:
            messages.error(request, "Your cart is empty.")
            return redirect('core:checkout')

        # Process form data (like billing and shipping details)
        billing_details = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip'),
            'country': request.POST.get('country'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email'),
        }

        # Check for missing billing details
        if not all(billing_details.values()):
            messages.error(request, "Please fill out all required fields.")
            return redirect('core:checkout')

        # Create an Order object
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,  # Add user if authenticated
            order_date=timezone.now(),
            total_amount=calculate_total_cart_amount(cart_data),
            **billing_details  # Save billing details in the order model
        )

        # Create OrderItem objects for each item in the cart
        for product_id, item in cart_data.items():
            OrderItem.objects.create(
                order=order,
                product_id=product_id,
                product_name=item['title'],
                product_price=item['price'],
                quantity=item['qty'],
                product_image=item['image'],
            )

        # Clear the cart after the order is placed
        del request.session['cart_data_obj']
        request.session.modified = True

        # Display success message
        messages.success(request, "Your order has been placed successfully.")

        # Redirect to order confirmation page or home page
        return redirect('core:order-confirmation')

    else:
        return redirect('core:checkout')

def calculate_total_cart_amount(cart_data):
    total = 0
    for item in cart_data.values():
        total += int(item['qty']) * float(item['price'])
    return total

def order_confirmation(request):
    return render(request, 'core/order_confirmation.html')