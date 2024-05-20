from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import Restaurant, Customer, Rider, User

@login_required
def dashboard(request):
    restaurants_count = Restaurant.objects.count()
    customers_count = Customer.objects.count()
    riders_count = Rider.objects.count()
    context = {
        'restaurants_count': restaurants_count,
        'customers_count': customers_count,
        'riders_count': riders_count
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def view_users(request):
    users = User.objects.all()
    users = User.objects.exclude(pk=request.user.pk)
    return render(request, 'view_users.html', {'users': users})

@login_required
def view_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'view_restaurants.html', {'restaurants': restaurants})

@login_required
def view_customers(request):
    customers = Customer.objects.all()
    return render(request, 'view_customers.html', {'customers': customers})

@login_required
def view_riders(request):
    riders = Rider.objects.all()
    return render(request, 'view_riders.html', {'riders': riders})


def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('view_users')
    return render(request, 'view_restaurants.html')

def delete_restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    if request.method == 'POST':
        restaurant.delete()
        return redirect('view_restaurants')
    return render(request, 'view_restaurants.html')

def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        customer.delete()
        return redirect('view_customers')
    return render(request, 'view_customers.html')

def delete_rider(request, id):
    rider= get_object_or_404(Rider, id=id)
    if request.method == 'POST':
        rider.delete()
        return redirect('view_riders')
    return render(request, 'view_riders.html')