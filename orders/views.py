from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from profiles.models import VoiceActorProfile
from .models import Order
from .forms import OrderForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY





@login_required
def create_order(request, actor_id):
    actor = get_object_or_404(VoiceActorProfile, id=actor_id)

    if request.user == actor.user:
        messages.error(request, 'O\'zingizga buyurtma bera olmaysiz!')
        return redirect('actor_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.actor = actor
            order.save()
            messages.success(request, 'Buyurtma muvaffaqiyatli yuborildi!')
            return redirect('my_orders')
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {
        'form': form,
        'actor': actor
    })


@login_required
def my_orders(request):
    if request.user.is_client():
        orders = Order.objects.filter(
            client=request.user
        ).select_related('actor__user').order_by('-created_at')
    else:
        orders = Order.objects.filter(
            actor__user=request.user
        ).select_related('client').order_by('-created_at')

    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.actor.user:
        messages.error(request, 'Ruxsat yo\'q!')
        return redirect('my_orders')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        delivered_file = request.FILES.get('delivered_file')

        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            if delivered_file:
                order.delivered_file = delivered_file
            order.save()
            messages.success(request, 'Status yangilandi!')

    return redirect('my_orders')



@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, client=request.user)

    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': order.title,
                            'description': f'{order.word_count} words · {order.actor.user.username}',
                        },
                        'unit_amount': int(order.total_price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(
                    f'/orders/payment-success/{order.id}/'
                ),
                cancel_url=request.build_absolute_uri('/orders/my-orders/'),
            )
            return redirect(checkout_session.url)
        except Exception as e:
            messages.error(request, f'Xato: {str(e)}')
            return redirect('my_orders')

    return render(request, 'orders/payment.html', {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, client=request.user)
    order.status = 'accepted'
    order.save()
    messages.success(request, 'To\'lov muvaffaqiyatli amalga oshirildi!')
    return redirect('my_orders')