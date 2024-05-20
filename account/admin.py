from django.contrib import admin
from .models import User, Customer, Restaurant, Rider

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'contact_number', 'default_address']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['user', 'resto_image','name', 'contact_number', 'address', 'business_hours', 'resto_qrcode']

@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'contact_number', 'driver_license', 'age']
