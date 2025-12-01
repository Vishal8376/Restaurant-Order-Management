from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import SignUpForm
from .models import MenuItem, Order, Payment, UserProfile
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template


# ---------- Signals for UserProfile creation ----------
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='customer')  # default to customer


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()


# ---------- Menu View ----------
from django.shortcuts import render
from .models import MenuItem

def menu_view(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'core/menu.html', {'menu_items': menu_items})


# ---------- Signup ----------
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        role = request.POST.get('role')
        if form.is_valid():
            user = form.save()
            # Don’t create a new profile, just update existing one
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.role = role if role else 'customer'
            user_profile.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            # Form has errors, add them to messages
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        field_name = field.replace('_', ' ').title()
                        messages.error(request, f"{field_name}: {error}")
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})


# ---------- Login ----------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ Check if user is superuser FIRST
            if user.is_superuser:
                return redirect('admin_dashboard')

            # ✅ Then check custom role-based redirection
            elif hasattr(user, 'userprofile'):
                role = user.userprofile.role
                if role == 'admin':
                    return redirect('admin_dashboard')
                elif role == 'customer':
                    return redirect('customer_dashboard')
                else:
                    return redirect('menu')
            else:
                return redirect('menu')  # fallback

        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'core/login.html')


# ---------- Logout ----------
from django.contrib import messages
from django.contrib.auth import logout

def custom_logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


# ---------- Dashboard Redirection ----------
@login_required
def dashboard_redirect(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.role.lower() == 'admin':
            return redirect('admin_dashboard')
        else:
            return redirect('customer_dashboard')
    except UserProfile.DoesNotExist:
        # Create default profile if it doesn't exist
        UserProfile.objects.create(user=request.user, role='customer')
        return redirect('customer_dashboard')



from django.db.models import Sum

@login_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_revenue = Payment.objects.filter(status='Completed').aggregate(Sum('amount'))['amount__sum'] or 0
    pending_payments = Payment.objects.filter(status='Pending').count()
    menu_items = MenuItem.objects.count()
    
    recent_orders = Order.objects.all().order_by('-created_at')[:5]

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_payments': pending_payments,
        'menu_items': menu_items,
        'recent_orders': recent_orders,
    }
    return render(request, 'core/admin_dashboard.html', context)

@login_required
def customer_dashboard(request):
    return render(request, 'core/customer_dashboard.html')


# ---------- Place Order ----------
from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Order, OrderItem, Payment
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from decimal import Decimal
from .models import Payment

@login_required
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(user=request.user, total_amount=0)
            total = 0
            for item in MenuItem.objects.all():
                quantity = form.cleaned_data.get(f'item_{item.id}')
                if quantity and quantity > 0:
                    OrderItem.objects.create(order=order, menu_item=item, quantity=quantity)
                    total += item.price * quantity

            if total == 0:
                order.delete()
                messages.error(request, "Please select at least one item to order.")
                return redirect('place_order')

            order.total_amount = total
            order.save()

            Payment.objects.create(
                user=request.user,
                order=order,
                amount=total,
                status='Pending'
            )

            print("✅ Redirecting to payment page...")
            return redirect('payment', order_id=order.id)

        else:
            print("❌ Form errors:", form.errors)

    else:
        form = OrderForm()

    # Pass menu items to template for displaying images
    menu_items = MenuItem.objects.all()
    form_fields_with_items = []
    
    for field in form:
        menu_item = None
        if hasattr(form, '_menu_items') and field.name in form._menu_items:
            menu_item = form._menu_items[field.name]
        form_fields_with_items.append({
            'field': field,
            'menu_item': menu_item
        })

    return render(request, 'core/place_order.html', {
        'form': form,
        'form_fields_with_items': form_fields_with_items
    })


# ---------- List Orders ----------
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/orders.html', {'orders': orders})



# ---------- Order Confirmation ----------
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/confirmation.html', {'order': order})



# ---------- Make Payment ----------
from decimal import Decimal
@login_required
def make_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Check for existing payment
    payment = Payment.objects.filter(order=order, user=request.user).first()

    if request.method == 'POST':
        if payment:
            # Update existing payment
            payment.amount = Decimal(order.total_amount)
            payment.status = 'Completed'
            payment.payment_date = timezone.now()
            payment.save()
        else:
            # Create new if missing (for safety)
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                amount=Decimal(order.total_amount),
                status='Completed',
                payment_date=timezone.now()
            )

        messages.success(request, 'Payment successful!')
        return redirect('payment_success', payment_id=payment.id)

    # Payment history
    payment_history = Payment.objects.filter(user=request.user).order_by('-payment_date')

    return render(request, 'core/make_payment.html', {
        'order': order,
        'payment_history': payment_history
    })


# ---------- Payment Success (Optional Page) ----------
@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'core/confirmation.html', {'payment': payment})


# ---------- Payment List View (Optional if using only make_payment) ----------
@login_required
def payment_list(request):
    payments = Payment.objects.filter(user=request.user).order_by('-payment_date')
    return render(request, 'core/payments.html', {'payment_history': payments})


# ---------- Media File Handling ----------
# Media files are now served directly by Django through MEDIA_URL configuration
# Images are properly handled via ImageField in MenuItem model