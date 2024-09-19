from .models import Category, Product, Vendor

def default(request):
    categories = Category.objects.all()
    products = Product.objects.all().order_by("-id")
    vendors = Vendor.objects.all()
    
    
    return {
        'categories': categories,
        'products': products,
        'vendors': vendors,
    }

def cart_data(request):
    cart_total_amount = 0
    total_cart_items = 0
    cart_data_obj = {}

    if 'cart_data_obj' in request.session:
        cart_data_obj = request.session['cart_data_obj']
        for product_id, item in cart_data_obj.items():
            try:
                cart_total_amount += int(item['qty']) * float(item['price'])
            except (ValueError):
                continue
        
        total_cart_items = len(cart_data_obj)

    return {
        'cart_data': cart_data_obj,
        'totalcartitems': total_cart_items,
        'cart_total_amount': cart_total_amount,
    }

def wishlist_data(request):
    wishlist_data_obj = {}
    
    if 'wishlist_data_obj' in request.session:
        wishlist_data_obj = request.session['wishlist_data_obj']
    
    return {
        'wishlist_data': wishlist_data_obj,
    }