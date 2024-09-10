from django.contrib import admin
from . import models

# Inline for ProductImages
class ProductImagesAdmin(admin.TabularInline):
    model = models.ProductImages

# inline for ProductAdditionalInfo

# Product Admin
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['title', 'vendor', 'product_image', 'price', 'featured', 'product_status']


# Category Admin
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']

# Vendor Admin
@admin.register(models.Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']

# Card Order Admin
@admin.register(models.CardOrder)
class CardOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']

# Cart Order Items Admin
@admin.register(models.CartOrderItems)
class CardOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']

# Product Review Admin
@admin.register(models.ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating', 'reviewer']

# Wishlist Admin
@admin.register(models.Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']

# Address Admin
@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']
