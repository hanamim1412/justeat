from django.shortcuts import render, redirect, get_object_or_404
from transactions.models import Order, Payment
from transactions.models import  Rider
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
# Create your views here.
from django.db.models import Count, Sum

    
@login_required
def rider(request):
    user = request.user
    if user.is_rider:
        rider = get_object_or_404(Rider, user=user)
        
        payments = Payment.objects.filter(rider=rider, payment_status='PAID')
        booked_orders_count = payments.exclude(order__status='DELIVERED').count()
        delivered_orders_count = (
            payments.filter(order__status='DELIVERED')
            .values('order_id')
            .distinct()
            .count()
        )
        delivery_fee = 50  
        
        total_earnings = (booked_orders_count + delivered_orders_count) * delivery_fee
        
        context = {
            'order_count': payments.count(),
            'booked_orders_count': booked_orders_count,
            'delivered_orders_count': delivered_orders_count,
            'total_earnings': total_earnings,
        }
        return render(request, 'rider-home.html', context)
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('index')


@login_required
def rider_view_orders(request):
    user = request.user
    if user.is_rider:
        rider = get_object_or_404(Rider, user=user)
        payments = Payment.objects.filter(rider_id__isnull=True).exclude(order__status__in=['OUT_FOR_DELIVERY', 'DELIVERED'])
        return render(request, 'rider_view_orders.html', {'payments': payments})
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('index')


@login_required
def rider_booked(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        rider = request.user.rider

        if rider:
            try:
                payment = get_object_or_404(Payment, pk=payment_id)
                if payment.rider:
                    messages.error(request, 'This order is already booked by another rider.')
                else:
                    payment.rider = rider
                    payment.save()
                    messages.success(request, 'Order booked successfully.')
            except Payment.DoesNotExist:
                messages.error(request, 'Payment does not exist.')
        else:
            messages.error(request, 'Rider profile does not exist.')

    return redirect('rider_view_orders')

@login_required
def rider_cancel_booking(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        rider = request.user.rider

        if rider:
            try:
                payment = get_object_or_404(Payment, pk=payment_id, rider=rider)
                payment.rider = None 
                payment.save()
                messages.success(request, 'Booking canceled successfully.')
            except Payment.DoesNotExist:
                messages.error(request, 'Payment does not exist or you are not authorized to cancel it.')
        else:
            messages.error(request, 'Rider profile does not exist.')

    return redirect('view_booked_orders')

@login_required
def view_booked_orders(request):
    user = request.user
    if user.is_rider:
        rider = get_object_or_404(Rider, user=user)
        
        payments = Payment.objects.filter(rider=rider).exclude(
            order__status__in=['DELIVERED']
        )
        
        return render(request, 'view_booked_orders.html', {'payments': payments})
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('index')

@login_required
def delivered_orders(request):
    user = request.user
    if user.is_rider:
        rider = get_object_or_404(Rider, user=user)
        payments = Payment.objects.filter(
            rider=rider,
            payment_status='PAID',
            order__status__in=['DELIVERED']
        )
        
        return render(request, 'delivered_orders.html', {'payments': payments})
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('index')



@login_required
def rider_update_status(request):
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
            
    return redirect('view_booked_orders')

@login_required
def rider_update_payment_status(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        payment_status = request.POST.get('payment_status')
        
        payment = get_object_or_404(Payment, pk=payment_id)
        payment.payment_status = payment_status
        payment.save()

        messages.success(request, 'Payment status updated successfully.')
        
        return redirect('view_booked_orders')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('view_booked_orders')

@login_required
def rider_order_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    context = {
        'order': order
    }

    return render(request, 'rider_order_details.html', context)

@login_required
def rider_payment_details(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)

    context = {
        'payment': payment
    }

    return render(request, 'rider_payment_details.html', context)

@login_required
def rider_view_receipt(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    
    context = {
        'payment': payment
    }
    return render(request, 'rider_receipt.html', context)

