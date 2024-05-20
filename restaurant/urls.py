from django.urls import path
from . import views

urlpatterns = [
    path('restaurant/', views.restaurant, name='restaurant'),
    # Categories
    path('add_category/', views.add_category, name='add_category'),
    path('update_category/<int:id>/', views.update_category, name='update_category'),
    path('view_categories/', views.view_categories, name='view_categories'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    # Menu Items
    path('add_item/', views.add_menu_item, name='add_menu_item'),
    path('update_menu_item/<int:id>/', views.update_menu_item, name='update_menu_item'),
    path('view_menu_items/', views.view_menu_items, name='view_menu_items'),
    path('delete_menu_item/<int:id>/', views.delete_menu_item, name='delete_menu_item'),
    #orders
    path('view_orders/', views.view_orders, name='view_orders'),
    path('restaurant_orders_history/', views.restaurant_orders_history, name='restaurant_orders_history'),
    path('update_status/', views.update_status, name='update_status'),
    path('update_payment_status/', views.update_payment_status, name='update_payment_status'),
    path('order_details/<int:order_id>/', views.order_details, name='order_details'),
    path('payment_details/<int:payment_id>/', views.payment_details, name='payment_details'),
    path('view_receipt/<int:payment_id>/', views.restaurant_view_receipt, name='restaurant_view_receipt'),

]