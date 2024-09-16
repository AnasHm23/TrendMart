from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    # products
    path('products/', views.product_list, name='products'),
    path('product/<str:pid>', views.product_detail, name='product-detail'),
    
    # categories
    path('category/<str:cid>', views.category_products_list, name='category-products'),
    
    # vendors
    path('vendor/<str:vid>', views.vendor_products_list, name='vendor-products'),
    
    #search for a product
    path('search/', views.search_view, name='search'),
    path('filter/', views.filter_view, name='filter'),
    
    # cart
    path('add-to-cart/', views.add_to_cart, name="add-to-cart")
]
