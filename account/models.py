from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_customer = models.BooleanField('Is customer', default=False)
    is_restaurant = models.BooleanField('Is restaurant', default=False)
    is_rider = models.BooleanField('Is rider', default=False)
    
class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    business_hours = models.CharField(max_length=100)
    resto_image = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)
    resto_qrcode= models.ImageField(upload_to='qrcode_images/', null=True, blank=True)

class Rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    driver_license = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    rider_image = models.ImageField(upload_to='rider_images/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    default_address = models.CharField(max_length=255)
    customer_image = models.ImageField(upload_to='customer_images/', null=True, blank=True)
