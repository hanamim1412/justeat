from django.contrib import admin
from .models import Category, MenuItem, Order, Payment

admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant']

    
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description','price', 'get_category_name','get_resto_name','restaurant_id','image']
    def get_category_name(self, obj):
        return obj.category.name
    get_category_name.short_description = 'Category'
    
    def get_resto_name(self, obj):
        return obj.restaurant.name
    get_resto_name.short_description = 'Restaurant'

    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'get_fname', 
        'get_restaurant_name', 
        'get_menu_items', 
        'subtotal',
        'total_amount',
        'status', 
        'get_contact_number',
        'get_current_address',
        'order_date'
        ]
    
    def get_fname(self, obj):
        return obj.customer.first_name
    get_fname.short_description = 'Customer'
    def get_contact_number(self, obj):
        return obj.customer.contact_number
    get_contact_number.short_description = 'Contact number'
    def get_current_address(self, obj):
        return obj.customer.default_address
    get_current_address.short_description = 'Current Address'
    def get_restaurant_name(self, obj):
        return obj.restaurant.name
    get_restaurant_name.short_description = 'Restaurant'
    def get_menu_items(self, obj):
        items_display = []
        for item in obj.items:
            item_info = f"{item['name']} (x{item['quantity']}) - Price: {item['price']} - Subtotal: {item['subtotal']}"
            items_display.append(item_info)
        return ', '.join(items_display)
    get_menu_items.short_description = 'Menu Items'
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'get_fname',
        'get_restaurant_name',
        'get_order_items',
        'subtotal',
        'total_amount',
        'mop', 
        'image',
        'reference_number',
        'current_address',
        'note',
        'rider_name', 
        'rider_contact', 
        'order_status',
        'payment_status', 
        'payment_date']
    def get_fname(self, obj):
        return obj.customer.first_name
    get_fname.short_description = 'Customer'
    
    def get_restaurant_name(self, obj):
        return obj.restaurant.name
    get_restaurant_name.short_description = 'Restaurant'
    
    def get_order_items(self, obj):
        order = obj.order
        order_items = order.items

        if order_items:
            item_display = []
            for item in order_items:
                item_info = f"{item['name']} (x{item['quantity']}) - Price: {item['price']} - Subtotal: {item['subtotal']}"
                item_display.append(item_info)
            return ', '.join(item_display)
        else:
            return "No items found"

    get_order_items.short_description = 'Order Items'
    def subtotal(self, obj):
        order = obj.order
        return order.subtotal
    subtotal.short_description = 'Order Subtotal'

    def total_amount(self, obj):
        order = obj.order
        return order.total_amount
    total_amount.short_description = 'Order Total Amount'
    def order_status(self, obj):
        order = obj.order
        return order.status
    order_status.short_description = 'Order status'
    
    def rider_name(self, obj):
        return obj.rider.first_name if obj.rider else 'No Rider Assigned'
    rider_name.short_description = 'Rider Name'

    def rider_contact(self, obj):
        return obj.rider.contact_number if obj.rider else 'No Contact Available'
    rider_contact.short_description = 'Rider Contact'
 