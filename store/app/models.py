from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
# Create your models here.

#product details model
class Product(models.Model):
    PRODUCT_STATUS = (('available', 'Available'),('unavailable', 'Not Available'),)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()
    status = models.CharField(max_length=11,choices=PRODUCT_STATUS,default='available')
    image = models.ImageField(upload_to='./media', blank=True, null=True)
    def __str__(self):
        return str(self.name)
    
    #check the availability 
    def is_available (self):
        return self.status == 'available' 
    
    #update the item status dynamically 
    def save(self, *args, **kwargs):
        if self.stock > 0:
            self.status = 'available'
        else:
            self.status = 'unavailable'
        super(Product,self).save(*args, **kwargs)

#cart model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    def __str__(self):
        return f"Cart of {self.user.username} - {'Paid' if self.is_paid else 'Not Paid'}"
    
#cart items model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
