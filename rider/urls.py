from django.urls import path
from . import views

urlpatterns = [
    path('rider/', views.rider, name='rider'),
    path('rider_view_orders/', views.rider_view_orders, name='rider_view_orders'),
    path('rider_booked/', views.rider_booked, name='rider_booked'),
    path('rider_cancel_booking/', views.rider_cancel_booking, name='rider_cancel_booking'),
    path('view_booked_orders/', views.view_booked_orders, name='view_booked_orders'),
    path('delivered_orders/', views.delivered_orders, name='delivered_orders'),
    path('rider_update_status/', views.rider_update_status, name='rider_update_status'),
    path('rider_update_payment_status/', views.rider_update_payment_status, name='rider_update_payment_status'),
    path('rider_order_details/<int:order_id>/', views.rider_order_details, name='rider_order_details'),
    path('rider_payment_details/<int:payment_id>/', views.rider_payment_details, name='rider_payment_details'),
    path('rider_view_receipt/<int:payment_id>/', views.rider_view_receipt, name='rider_view_receipt'),
]