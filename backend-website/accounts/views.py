from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Add this import
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from data.models import Plant, Order, OrderItem
from data.constants import PaymentStatus
from django.conf import settings
import razorpay
from .utils.emails import send_order_confirmation
from .forms import ShippingDetailsForm
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.template.defaultfilters import register
import os 
@login_required
def profile(request):
    if request.user.is_authenticated:
        return redirect('display')

@login_required
def profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html',{'user':request.user})
    else:
        return render(request,'login.html',{})
    
def home(request):
    return render(request, 'main.html', {})


def display(request):
    plants = Plant.objects.all()
    return render(request,'home/display.html', {'plants': plants})

@register.filter(name='jsonify')
def jsonify(value):
    return json.dumps(value, cls=DjangoJSONEncoder)


def SpecificPlant(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    similar_plants = Plant.objects.filter(Category=plant.Category).exclude(id=plant_id)
    
    # Convert cart data to JSON for JavaScript
    cart = request.session.get('cart', {})
    
    return render(request, 'home/specific_plant.html', {
        'plant': plant,
        'similar_plants': similar_plants,
    })

@login_required
def checkout(request,plant_id):
    plant = Plant.objects.get(id=plant_id)
    print(plant)
    return render(request, 'home/checkout.html', {'plant': plant})


@login_required
def add_to_cart(request, plant_id):
    cart = request.session.get('cart', {})
    plant_id = str(plant_id)
    
    # Set quantity to 1 if item doesn't exist, otherwise don't change
    if plant_id not in cart:
        cart[plant_id] = 1
    
    request.session['cart'] = cart
    request.session.modified = True
    
    return JsonResponse({
        'cart_count': sum(cart.values()),
        'message': 'Item added to cart successfully'
    })
@login_required
def update_cart_quantity(request, plant_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        try:
            quantity = int(request.POST.get('quantity', 1))
            plant_id = str(plant_id)
            
            if quantity > 0:
                cart[plant_id] = quantity
            else:
                del cart[plant_id]
                
            request.session['cart'] = cart
            request.session.modified = True
            
            # Recalculate total
            total = 0
            for pid, qty in cart.items():
                plant = get_object_or_404(Plant, id=pid)
                total += plant.price * qty
            
            return JsonResponse({
                'cart_count': sum(cart.values()),
                'total': total
            })
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid quantity'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    
    for pid, qty in cart.items():
        try:
            plant = get_object_or_404(Plant, id=pid)
            line_total = float(plant.price) * int(qty)
            items.append({
                'plant': plant,
                'quantity': qty,
                'line_total': line_total,
            })
            total += line_total
        except Plant.DoesNotExist:
            continue

    context = {
        'cart_items': items,
        'total_amount': total,  # Changed from order.total to total_amount
    }
    
    return render(request, 'home/checkout.html', context)
@login_required
def remove_from_cart(request, plant_id):
    cart = request.session.get('cart', {})
    plant_id = str(plant_id)
    
    if plant_id in cart:
        del cart[plant_id]
        request.session['cart'] = cart
        request.session.modified = True
        
        # Recalculate total after removal
        total = sum(get_object_or_404(Plant, id=pid).price * qty 
                   for pid, qty in cart.items())
        
        return JsonResponse({
            'cart_count': sum(cart.values()),
            'total': total,
            'message': 'Item removed from cart'
        })
    
    return JsonResponse({
        'error': 'Item not found in cart'
    }, status=404)

@login_required
def shipping_details(request):
    if request.method == 'POST':
        form = ShippingDetailsForm(request.POST, user=request.user)
        if form.is_valid():
            request.session['shipping_details'] = form.cleaned_data
            return redirect('order_payment')
    else:
        form = ShippingDetailsForm(user=request.user)

    # Get cart from session
    cart = request.session.get('cart', {})
    
    # Calculate total amount from cart items
    total_amount = 0
    cart_items = []
    
    for plant_id, quantity in cart.items():
        try:
            plant = Plant.objects.get(id=plant_id)
            subtotal = plant.price * quantity
            total_amount += subtotal
            cart_items.append({
                'plant': plant,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except Plant.DoesNotExist:
            continue

    return render(request, 'shipping_details.html', {
        'form': form,
        'cart_items': cart_items,
        'total_amount': total_amount
    })

@login_required
def order_payment(request):
    if request.method != 'POST':
        return redirect('cart_view')

    try:
        # Get cart and calculate total
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty")
            return redirect('cart_view')

        total = 0
        order_items = []
        
        for pid, qty in cart.items():
            try:
                plant = get_object_or_404(Plant, id=pid)
                item_total = float(plant.price) * int(qty)
                total += item_total
                order_items.append({
                    'plant': plant,
                    'quantity': qty,
                    'price': plant.price,
                    'total': item_total
                })
            except Plant.DoesNotExist:
                continue

        # Verify total matches form submission
        form_total = float(request.POST.get('total_amount', 0))
        if abs(form_total - total) > 0.01:  # Allow for small floating point differences
            messages.error(request, "Order total mismatch. Please try again.")
            return redirect('cart_view')

        # Initialize Razorpay
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Create Razorpay order (amount in paise)
        payment_order = client.order.create({
            "amount": int(total * 100),
            "currency": "INR",
            "payment_capture": "1"
        })

        # Create order in database
        order = Order.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phone_number'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            amount=total,
            provider_order_id=payment_order['id']
        )

        # Create order items
        for item in order_items:
            OrderItem.objects.create(
                order=order,
                plant=item['plant'],
                plant_name=item['plant'].name,
                quantity=item['quantity'],
                price=item['price']
            )

        # Prepare payment context
        context = {
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "order": order,
            "callback_url": request.build_absolute_uri(reverse('payment_callback')),
            "total_amount": total,
            "order_items": order_items
        }
        
        return render(request, "payment.html", context)

    except Exception as e:
        print(f"Payment initialization error: {str(e)}")
        messages.error(request, "Unable to initialize payment. Please try again.")
        return redirect('cart_view')

@login_required
@csrf_exempt
def callback(request):
    payment_id = request.POST.get("razorpay_payment_id") or request.GET.get("razorpay_payment_id", "")
    order_id = request.POST.get("razorpay_order_id") or request.GET.get("razorpay_order_id", "")
    signature = request.POST.get("razorpay_signature") or request.GET.get("razorpay_signature", "")

    try:
        if not all([payment_id, order_id, signature]):
            return render(request, "callback.html", {
                "status": "failure",
                "message": "Missing payment parameters"
            })

        order = Order.objects.get(provider_order_id=order_id)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        params_dict = {
            'razorpay_payment_id': payment_id,
            'razorpay_order_id': order_id,
            'razorpay_signature': signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)
            order.payment_id = payment_id
            order.signature_id = signature
            order.status = PaymentStatus.SUCCESS
            order.save()
            
            # Try to send email but don't fail if it doesn't work
            email_sent = send_order_confirmation(order, request.user)
            
            # Clear cart and update inventory
            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True
            
            return render(request, "callback.html", {
                "status": "success",
                "message": "Payment successful!" + (
                    "" if email_sent else " (Order confirmation email could not be sent)"
                ),
                "order_id": order.id,
                "amount": order.amount,
                "user": request.user
            })
            
        except Exception as e:
            print(f"Payment verification failed: {e}")
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", {
                "status": "failure",
                "message": "Payment verification failed"
            })
            
    except Order.DoesNotExist:
        return render(request, "callback.html", {
            "status": "failure",
            "message": "Order not found"
        })
    except Exception as e:
        print(f"Callback processing failed: {e}")
        return render(request, "callback.html", {
            "status": "failure",
            "message": "An error occurred during payment processing"
        })
