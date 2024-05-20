from django.shortcuts import render, redirect, get_object_or_404
from transactions.models import Category, MenuItem, Order, Payment
from transactions.models import Restaurant, Rider, Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from datetime import timedelta
from django.utils import timezone
from collections import Counter
from operator import itemgetter
from collections import defaultdict

@login_required
def restaurant(request):  # Dashboard
    user = request.user
    if user.is_restaurant:
        restaurant = get_object_or_404(Restaurant, user=user)
        
        category_count = Category.objects.filter(restaurant=restaurant).count()
        menu_item_count = MenuItem.objects.filter(restaurant=restaurant).count()
        order_count = Order.objects.filter(restaurant=restaurant).count()
        total_revenue = Order.objects.filter(restaurant=restaurant).aggregate(Sum('total_amount'))['total_amount__sum']
        total_revenue = total_revenue if total_revenue else 0
        
        # Calculate orders by status
        status_counts = Order.objects.filter(restaurant=restaurant).values('status').annotate(count=Count('status'))
        order_statuses = [status['status'] for status in status_counts]
        order_counts = [status['count'] for status in status_counts]
        
        # Calculate total customers who ordered
        total_customers = Order.objects.filter(restaurant=restaurant).values('customer').distinct().count()
       
        payments = Payment.objects.filter(restaurant=restaurant, payment_status='PAID')
        payment_by_mode = {}
        for payment in payments:
            mode = dict(Payment.MODE_OF_PAYMENT_CHOICES).get(payment.mop, payment.mop)
            if mode in payment_by_mode:
                payment_by_mode[mode] += payment.order.total_amount
            else:
                payment_by_mode[mode] = payment.order.total_amount

        payment_modes = list(payment_by_mode.keys())
        payment_totals = [float(total) for total in payment_by_mode.values()]
        
        
        context = {
            'category_count': category_count,
            'menu_item_count': menu_item_count,
            'order_count': order_count,
            'total_revenue': total_revenue,
            'total_customers': total_customers,
            'order_statuses': order_statuses,
            'order_counts': order_counts,
            'payment_modes': payment_modes,
            'payment_totals': payment_totals,
        }
        return render(request, 'restaurant-home.html', context)
    else:
        return redirect('index')
    
    
@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        user = request.user
        if user.is_restaurant:
            restaurant = get_object_or_404(Restaurant, user=user)
            Category.objects.create(name=name, restaurant=restaurant)
            messages.success(request, f"Category Added successfully.")
            return redirect('view_categories')
    return render(request, 'category/add_category.html')

@login_required
def update_category(request, id):
    user = request.user
    if user.is_restaurant:
        restaurant = get_object_or_404(Restaurant, user=user)
        category = get_object_or_404(Category, id=id, restaurant=restaurant)
        if request.method == 'POST':
            category.name = request.POST.get('name')
            category.save()
            messages.success(request, f"Category Updated successfully.")
            return redirect('view_categories')
    return render(request, 'category/update_category.html', {'category': category})

@login_required
def view_categories(request):
    user = request.user
    if user.is_restaurant:
        restaurant = get_object_or_404(Restaurant, user=user)
        categories = Category.objects.filter(restaurant=restaurant)
        return render(request, 'category/view_categories.html', {'categories': categories})
    else:
        return redirect('index')

@login_required
def delete_category(request, id):
    user = request.user
    if user.is_restaurant:
        restaurant = get_object_or_404(Restaurant, user=user)
        category = get_object_or_404(Category, id=id, restaurant=restaurant)
        if request.method == 'POST':
            category.delete()
            messages.success(request, f"Category Deleted successfully.")
            return redirect('view_categories')
    return render(request, 'category/view_categories.html')

# MenuItem operations
@login_required
def add_menu_item(request):
    user = request.user
    if user.is_restaurant:
        restaurant = get_object_or_404(Restaurant, user=user)
        if request.method == 'POST':
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            upload = request.FILES.get('image')
            category_id = request.POST.get('category')
            category = get_object_or_404(Category, id=category_id, restaurant=restaurant)
            
            MenuItem.objects.create(
                restaurant=restaurant,
                name=name,
                description=description,
                price=price,
                image=upload,
                category=category
            )
            messages.success(request, f"Menu Added successfully.")
            return redirect('view_menu_items')
        else:
            categories = Category.objects.filter(restaurant=restaurant)
            return render(request, 'menuItem/add_item.html', {'categories': categories})
    else:
        return redirect('index')

@login_required
def update_menu_item(request, id):
    user = request.user
    if user.is_restaurant:
        restaurant = get_object_or_404(Restaurant, user=user)
        categories = Category.objects.filter(restaurant=restaurant)
        menu_item = get_object_or_404(MenuItem, id=id, category__restaurant=restaurant)
        
        if request.method == 'POST':
            menu_item.name = request.POST.get('name')
            menu_item.description = request.POST.get('description')
            menu_item.price = request.POST.get('price')
            
            if 'image' in request.FILES:
                menu_item.image = request.FILES['image']
                
            category_id = request.POST.get('category')
            category = get_object_or_404(Category, id=category_id, restaurant=restaurant)
            menu_item.category = category
            menu_item.restaurant = restaurant
            menu_item.save()
            messages.success(request, f"Menu Item Updated successfully.")
            return redirect('view_menu_items')
        return render(request, 'menuItem/update_item.html', {'menu_item': menu_item, 'categories': categories})

@login_required
def view_menu_items(request):
    user = request.user
    if user.is_restaurant:
        restaurant = get_object_or_404(Restaurant, user=user)
        menu_items = MenuItem.objects.filter(category__restaurant=restaurant)
        return render(request, 'menuItem/view_items.html', {'menu_items': menu_items})
    else:
        return redirect('index')

@login_required
def delete_menu_item(request, id):
    user = request.user
    if user.is_restaurant:
        restaurant = get_object_or_404(Restaurant, user=user)
        menu_item = get_object_or_404(MenuItem, id=id, category__restaurant=restaurant)
        if request.method == 'POST':
            menu_item.delete()
            messages.success(request, f"Menu Item Deleted successfully.")
            return redirect('view_menu_items')
    return render(request, 'menuItem/view_items.html')

# view Orders that has payment data
@login_required
def view_orders(request):
    user = request.user
    if user.is_restaurant:
        restaurant = get_object_or_404(Restaurant, user=user)
        
        # Filter out orders with status 'Out for Delivery' and 'Delivered'
        payments = Payment.objects.filter(order__restaurant=restaurant).exclude(
            order__status__in=['OUT_FOR_DELIVERY', 'DELIVERED']
        )
        
        return render(request, 'orders/view_orders.html', {'payments': payments})
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('index')

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    context = {
        'order': order
    }

    return render(request, 'orders/order_details.html', context)


@login_required
def payment_details(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)

    context = {
        'payment': payment
    }

    return render(request, 'orders/payment_details.html', context)

def update_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        try:
            order = get_object_or_404(Order, pk=order_id)
            order.status = status
            order.save()
            messages.success(request, f"Order #{order_id} status updated successfully.")
        except Order.DoesNotExist:
            messages.error(request, f"Order with ID #{order_id} does not exist.")
    return redirect('view_orders')

@login_required
def update_payment_status(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        payment_status = request.POST.get('payment_status')
        
        payment = get_object_or_404(Payment, pk=payment_id)
        payment.payment_status = payment_status
        payment.save()

        messages.success(request, 'Payment status updated successfully.')
        
        return redirect('view_orders')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('view_orders')
    

@login_required(login_url='/login/')
def restaurant_view_receipt(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    
    context = {
        'payment': payment
    }
    return render(request, 'orders/restaurant_receipt.html', context)


@login_required
def restaurant_orders_history(request):
    user = request.user
    if user.is_restaurant:
        restaurant = get_object_or_404(Restaurant, user=user)
        
        payments = Payment.objects.filter(
            order__restaurant=restaurant,
            payment_status='PAID',
            order__status='DELIVERED'
        )
        
        return render(request, 'orders/restaurant_orders_history.html', {'payments': payments})
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('index')
