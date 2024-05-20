from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from transactions.models import Category, Order, Payment, MenuItem
from account.models import Restaurant, Customer, Rider
import uuid
from django.db.models import Q
from collections import defaultdict
from decimal import Decimal
from django.contrib.auth.models import User
from account.forms import UpdateProfileForm

@login_required
def update_profile(request):
    user = request.user
    user_type = None
    
    if hasattr(user, 'customer'):
        user_type = 'customer'
    
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=user, user_type=user_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('update_profile')
    else:
        form = UpdateProfileForm(instance=user, user_type=user_type)
    
    return render(request, 'update_profile.html', {'form': form})


def index(request):
    categories = Category.objects.all()
    restaurants = Restaurant.objects.all()
    return render(request, 'index.html', {'categories': categories, 'restaurants': restaurants})

@login_required
def customer(request):
    categories = Category.objects.all()
    restaurants = Restaurant.objects.all()
    return render(request,'index.html', {'categories': categories, 'restaurants': restaurants})

def restaurant_menu_items(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    categories = Category.objects.filter(restaurant=restaurant)
    
    for category in categories:
        category.menu_items = MenuItem.objects.filter(category=category)
    
    context = {
        'restaurant': restaurant,
        'categories': categories,
        'restaurant_id': restaurant_id,
    }
    return render(request, 'menu_items.html', context)


@login_required(login_url='/login/')
def add_order(request):
    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item_id')
        restaurant_id = request.POST.get('restaurant_id')
        quantity = int(request.POST.get('quantity', 1))

        if not (menu_item_id and restaurant_id):
            return HttpResponseBadRequest("Menu item ID and restaurant ID are required.")

        menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

        order, created = Order.objects.get_or_create(
            customer=request.user.customer,
            restaurant=restaurant,
            status='PENDING',
            payment__isnull=True,  
            defaults={'items': [], 'total_amount': Decimal(0)}
        )

        items = order.items
        updated = False
        for item in items:
            if item['menu_item_id'] == menu_item_id:
                item['quantity'] += quantity
                item['subtotal'] = float(item['quantity']) * float(menu_item.price)
                updated = True
                break

        if not updated:
            items.append({
                'menu_item_id': menu_item_id,
                'name': menu_item.name,
                'description': menu_item.description,
                'image_url': menu_item.image.url,
                'quantity': quantity,
                'price': float(menu_item.price),
                'subtotal': float(quantity * menu_item.price),
            })

        # Calculate the total price
        subtotal = sum(item['subtotal'] for item in items)
        delivery_fee = 50
        total_price = subtotal + delivery_fee

        order.items = items
        order.total_amount = total_price
        order.save()

        messages.success(request, "Food item ordered successfully.")
        return redirect('customer_view_orders')

    else:
        return redirect('index')

@login_required(login_url='/login/')
def customer_view_orders(request):
    if request.user.is_authenticated and hasattr(request.user, 'customer'):
        excluded_payment_statuses = ['PAID', 'PENDING', 'FAILED']
        
        orders = Order.objects.filter(
            customer=request.user.customer
        ).exclude(
            Q(payment__payment_status__in=excluded_payment_statuses)
        )
        
        restaurant_order_items = defaultdict(list)
        subtotal_per_group = {}
        
        for order in orders:
            restaurant_order_items[order.restaurant].append(order)
            subtotal = sum(item['subtotal'] for item in order.items)
            order.subtotal = subtotal 
            order.save()
            if order.restaurant in subtotal_per_group:
                subtotal_per_group[order.restaurant] += subtotal
            else:
                subtotal_per_group[order.restaurant] = subtotal

        context = {
            'restaurant_order_items': dict(restaurant_order_items),
            'subtotal_per_group': subtotal_per_group,
            'order_items_count': orders.count()
        }
        request.session['order_items_count'] = context['order_items_count']
        return render(request, 'customer_view_orders.html', context)
    
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('index')

from django.http import JsonResponse

@login_required(login_url='/login/')
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    item_id = request.POST.get('item_id')
    
    items = order.items
    
    item_found = False
    for idx, item in enumerate(items):
        if str(item['menu_item_id']) == item_id:  
            items.pop(idx)
            item_found = True
            break
    
    if not item_found:
        return JsonResponse({'error': 'Item not found in order.'}, status=400)
    
    order.items = items
    
    if not items: 
        order.delete()  
        messages.success(request, 'Removed order completely.')
        return redirect('customer_view_orders')
    
    order.save()
    
    messages.success(request, 'Removed order item successfully.')
    return redirect('customer_view_orders')

@login_required(login_url='/login/')
def customer_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = get_object_or_404(Order, pk=order_id, customer=request.user.customer)
            restaurant = order.restaurant

            subtotal = sum(item['subtotal'] for item in order.items)
            delivery_fee = 50
            total_price = subtotal + delivery_fee

            context = {
                'restaurant': restaurant,
                'order_items': order.items,  # items is a list of order items
                'order_id': order_id,
                'subtotal': subtotal,
                'delivery_fee': delivery_fee,
                'total_price': total_price,
                'customer': request.user.customer,
            }
            return render(request, 'customer_payment.html', context)

        except Order.DoesNotExist:
            messages.error(request, 'Order does not exist.')
            return redirect('customer_view_orders')

    return redirect('customer_view_orders')


from django.db import transaction

@login_required(login_url='/login/')
def process_payment(request, order_id):
    if request.method == 'POST':
        mode_of_payment = request.POST.get('mode_of_payment')
        note = request.POST.get('note')

        try:
            order = get_object_or_404(Order, pk=order_id, customer=request.user.customer)
            restaurant = order.restaurant
            default_address = request.user.customer.default_address
            new_address = request.POST.get('new_address')

            with transaction.atomic():
                payment = Payment.objects.create(
                    customer=request.user.customer,
                    restaurant=restaurant,
                    mop=mode_of_payment,
                    note=note,
                    payment_status='PENDING',
                    current_address=new_address if new_address else default_address
                
                )

                payment.order = order
                payment.save()

                if mode_of_payment == 'GCASH':
                    proof_payment = request.FILES.get('proof_payment')
                    reference_number = request.POST.get('reference_number')

                    if not proof_payment or not reference_number:
                        messages.error(request, 'Please provide proof of payment and reference number.')
                        return redirect('customer_payment', order_id=order_id)

                    payment.image = proof_payment
                    payment.reference_number = reference_number
                    payment.payment_status = 'PAID'
                    payment.save()

                    messages.success(request, 'Payment successful.')

                elif mode_of_payment == 'CASH':
                    messages.success(request, 'Payment details submitted. Waiting for rider confirmation.')

                return redirect('customer_purchased')

        except (Restaurant.DoesNotExist, Order.DoesNotExist):
            messages.error(request, 'Restaurant or order does not exist.')
            return redirect('customer_view_orders')

    else:
        messages.error(request, 'Invalid request method.')
        return redirect('customer_view_orders')


@login_required(login_url='/login/')
def customer_purchased(request):
    purchased_orders = Payment.objects.filter(customer=request.user.customer, payment_status__in=['PENDING', 'PAID', 'FAILED'])

    context = {
        'purchased_orders': purchased_orders
    }

    return render(request, 'customer_purchased.html', context)

@login_required(login_url='/login/')
def receipt_view(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, customer=request.user.customer)

    context = {
        'payment': payment,
        'customer_fname': request.user.customer.first_name,
        'customer_lname': request.user.customer.last_name,
        'customer_address': payment.current_address if payment.current_address else request.user.customer.default_address,
        'customer_contact_number': request.user.customer.contact_number,
    }
    return render(request, 'receipt.html', context)

