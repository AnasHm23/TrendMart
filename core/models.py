from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User


STATUS_CHOICE = (
    ("Process", "Processed"),
    ("shipped", "Shipped"),
    ("Delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

def user_directory_path(instace, filename):
    return f'user_{instace.user.id}/{filename}'


#############################################
################ Models #####################
#############################################

############################## category model setting up ############################
class Category(models.Model):
    category_id = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="food")
    image = models.ImageField(upload_to="category", default="category.jpg")
    
    class Meta:
        verbose_name_plural = "categories"
        
    def category_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />' )
    
    def __str__(self):
        return self.title 


class Tags(models.Model):
    pass


####################### Vendor Model setting up ########################
class Vendor(models.Model):    
    vendor_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=50, default="Trendify")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    description = models.TextField(null=True, blank=True, default="I am an Excellent vendor")
    address = models.CharField(max_length=100, default="123 main street")
    contact = models.CharField(max_length=100, default="+123 (456) 789")
    
    rating = models.IntegerField(choices=RATING, default=None)
    
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100 , default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = "Vendors"
    
    def vendor_image(self):
        if self.image and hasattr(self.image, 'url'):
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" style="border-radius: 50%;"/>')
        else:
            return "No Image Available"

    def __str__(self) -> str:
        return self.title
    
    def get_rating_display(self):
        rating_dict = dict(RATING)
        return rating_dict.get(self.rating, '')

#################### Product Model setting up #####################

class Product(models.Model):
    product_id = ShortUUIDField(unique=True, length=10, max_length=30, alphabet="abcdefgh12345")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="products")
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="product")
    
    price = models.DecimalField(max_digits=9999, decimal_places=2, default ="1.99")
    old_price = models.DecimalField(max_digits=9999, decimal_places=2, default ="2.99")
    
    specifications = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "products"
        
    def product_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />' )
    
    def __str__(self):
        return self.title 

    def get_percentage(self):
        discount = ((self.old_price - self.price) / self.old_price) * 100
        return f"-{round(discount)}%"
    
class ProductImages(models.Model):
    product_images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "product Images"
    
    
############################# card, order, order items model setting up ################################    
class CardOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9999999, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=10, default="Processing")
    
    class Meta:
        verbose_name_plural = "Card Orders"
        
class CartOrderItems(models.Model):
    order = models.ForeignKey(CardOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9999, decimal_places=2, default ="1.99")
    total = models.DecimalField(max_digits=9999, decimal_places=2, default ="1.99")
    
    class Meta:
        verbose_name_plural = "Cart Order Items"
    
    def order_img(self):
        return mark_safe(f"<img src='/media/{self.image}' width='50' height='50' ")
        

########################## Product review, wishlists, address #####################
########################## Product review, wishlists, address #####################

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    reviewer = models.CharField(max_length=100 , null=False, default="Anonymous")
    reviewer_image = models.ImageField(upload_to="review", default="reviewer.jpg")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Reviews"
        
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"
        
    def __str__(self):
        return self.product.title
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"
        

########################## Orders #####################
########################## OrderItems #####################

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} - {self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    product_image = models.URLField()

    def __str__(self):
        return f"{self.product_name} (Order {self.order.id})"
