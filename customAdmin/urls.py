from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('view_users/', views.view_users, name="view_users"),
    path('view_customers/', views.view_customers, name="view_customers"),
    path('view_restaurants/', views.view_restaurants, name="view_restaurants"),
    path('view_riders/', views.view_riders, name="view_riders"),
    path('delete_user/<int:id>/', views.delete_user, name="delete_user"),
    path('delete_customer/<int:id>/', views.delete_customer, name="delete_customer"),
    path('delete_restaurant/<int:id>/', views.delete_restaurant, name="delete_restaurant"),
    path('delete_rider/<int:id>/', views.delete_rider, name="delete_rider"),
]