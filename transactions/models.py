from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from account.models import Restaurant, Customer, Rider
from decimal import Decimal
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} {self.restaurant.name}"

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_item_images/')
    
    def __str__(self):
        return f"{self.name} {self.description} {self.restaurant} {self.price} {self.image} {self.category.name}"

class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True, blank=True)
    items = models.JSONField(null=True)
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('PREPARING', 'Preparing'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    contact_num = models.PositiveIntegerField(null=True)
    
    def __str__(self):
        return f'{self.restaurant} {self.customer} {self.items} {self.status} {self.quantity} {self.total_amount}'

   
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, null=True, blank=True)
    current_address = models.CharField(max_length=255, null=True)
    
    MODE_OF_PAYMENT_CHOICES = [
        ('CASH', 'Cash'),
        ('GCASH', 'Gcash'),
    ]
    mop = models.CharField(max_length=10, choices=MODE_OF_PAYMENT_CHOICES)
    note = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='payment_images/', null=True, blank=True)
    reference_number = models.CharField(max_length=50, null=True)
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    payment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.payment_status == 'PAID' and not self.payment_date:
            self.payment_date = timezone.now()  
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.customer} {self.order} {self.mop} {self.note} {self.rider} {self.image} {self.reference_number} {self.payment_status} {self.payment_date}" 
