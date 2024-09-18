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