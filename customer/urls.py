from django.urls import path
from . import views
from account.views import login_view, register, logout_view

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', login_view, name='login_view'),
    path('register/', register, name='register'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('logout/', logout_view, name='logout'),
    path('customer/', views.customer, name='customer'),
    path('restaurant/<int:restaurant_id>/menu_items/', views.restaurant_menu_items, name='restaurant_menu_items'),
    path('add_order/', views.add_order, name='add_order'),
    path('customer_view_orders/', views.customer_view_orders, name='customer_view_orders'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('customer_payment/', views.customer_payment, name='customer_payment'),
    path('process_payment/<int:order_id>/', views.process_payment, name='process_payment'),
    path('customer_purchased/', views.customer_purchased, name='customer_purchased'),
    path('receipt/<int:payment_id>/', views.receipt_view, name='receipt'),
]