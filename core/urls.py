from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='products'),
    path('category/<str:cid>', views.category_products_list, name='category-products'),
    path('vendor/<str:vid>', views.vendor_products_list, name='vendor-products'),
]
