from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import Watch, Cart, Order, Address, Wishlist, ContactMessage
from .forms import (
    CustomerRegistrationForm,
    LoginForm,
    AddressForm,
    EditProfileForm,
    WatchForm,
)
from django.contrib.admin.views.decorators import staff_member_required


# ---------------- HOME ----------------
def home(request):
    watches = Watch.objects.all().order_by('-id')
    return render(request, 'watches/home.html', {'watches': watches})


# ---------------- ABOUT ----------------
def about(request):
    return render(request, 'watches/about.html')


# ---------------- CONTACT ----------------
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject", "")
        message_text = request.POST.get("message")

        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text,
            )
            messages.success(
                request,
                "Thank you for contacting us. We will get back to you soon.",
            )
            return redirect("contact")
        else:
            messages.error(request, "Please fill in all the required fields.")

    return render(request, 'watches/contact.html')

def search(request):
    query = request.GET.get('q', '')
    watches = Watch.objects.filter(
        name__icontains=query
    ) | Watch.objects.filter(
        brand__icontains=query
    ) | Watch.objects.filter(
        category__icontains=query
    )
    return render(request, 'watches/search_results.html', {
        'watches': watches,
        'query': query
    })

# ---------------- ALL CATEGORIES ----------------
def all_categories(request):
    watches = Watch.objects.all()
    return render(request, 'watches/category.html', {
        'watches': watches,
        'category': 'All Watches'
    })


# ---------------- CATEGORY VIEW ----------------
class CategoryView(View):
    def get(self, request, category):
        watches = Watch.objects.filter(category=category)
        return render(request, 'watches/category.html', {
            'watches': watches,
            'category': category
        })


# ---------------- WATCH DETAIL ----------------
class WatchDetailView(View):
    def get(self, request, pk):
        watch = get_object_or_404(Watch, pk=pk)
        return render(request, 'watches/watch_detail.html', {
            'watch': watch
        })


# ---------------- REGISTER VIEW ----------------
def register(request):

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)   # Auto login after register
            messages.success(request, "Account created successfully!")
            return redirect('home')

    else:
        form = CustomerRegistrationForm()

    return render(request, 'watches/register.html', {'form': form})


# ---------------- LOGIN VIEW ----------------
def user_login(request):

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

    else:
        form = LoginForm()

    return render(request, "watches/login.html", {"form": form})


# ---------------- LOGOUT VIEW ----------------
def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(
        request,
        "watches/profile.html",
        {
            "addresses": addresses,
            "orders": orders,
        },
    )


@login_required
def add_address(request):

    if request.method == "POST":
        form = AddressForm(request.POST)

        if form.is_valid():
            addr = form.save(commit=False)
            addr.user = request.user
            addr.save()
            return redirect('address')

    else:
        form = AddressForm()

    return render(request, "watches/add_address.html", {'form': form})


@login_required
def address(request):
    add = Address.objects.filter(user=request.user)
    return render(request, "watches/address.html", {'add': add})


@login_required
def edit_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('address')
    else:
        form = AddressForm(instance=address)

    return render(request, 'watches/add_address.html', {'form': form})


@login_required
def delete_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)
    address.delete()
    return redirect('address')


@login_required
def edit_profile(request):

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'watches/edit_profile.html', {'form': form})


@login_required
def add_to_cart(request, watch_id):

    watch = get_object_or_404(Watch, id=watch_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        watch=watch
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')


@login_required
def view_cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.total_price()

    context = {
        'cart_items': cart_items,
        'total': total
    }

    return render(request, 'watches/cart.html', context)


@login_required
def remove_from_cart(request, cart_id):

    item = get_object_or_404(Cart, id=cart_id, user=request.user)
    item.delete()

    return redirect('view_cart')


@login_required
def increase_quantity(request, cart_id):

    cart = Cart.objects.get(id=cart_id)

    cart.quantity += 1
    cart.save()

    return redirect('view_cart')


@login_required
def decrease_quantity(request, cart_id):

    cart = Cart.objects.get(id=cart_id)

    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()
    else:
        cart.delete()

    return redirect('view_cart')


@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)
    addresses = Address.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.total_price()

    if request.method == 'POST':
        address_id = request.POST.get('address')
        payment_method = request.POST.get('payment_method', 'cod')
        address = get_object_or_404(Address, id=address_id, user=request.user)

        placed_orders = []
        for item in cart_items:
            order = Order.objects.create(
                user=request.user,
                watch=item.watch,
                quantity=item.quantity,
                price=item.total_price(),
                total_amount=item.total_price(),
                address=address,
                status=f"Confirmed ({payment_method.upper()})",
            )
            placed_orders.append(order)

        cart_items.delete()
        messages.success(request, "Order placed successfully!")
        return render(
            request,
            'watches/order_confirmation.html',
            {
                'orders': placed_orders,
                'payment_method': payment_method,
            },
        )

    context = {
        'cart_items': cart_items,
        'addresses': addresses,
        'total': total
    }

    return render(request, 'watches/checkout.html', context)


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related('watch')
    return render(
        request,
        'watches/wishlist.html',
        {
            'wishlist_items': items,
        },
    )


@login_required
def add_to_wishlist(request, watch_id):
    watch = get_object_or_404(Watch, id=watch_id)
    Wishlist.objects.get_or_create(user=request.user, watch=watch)
    messages.success(request, "Added to wishlist.")
    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, wishlist_id):
    item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    item.delete()
    messages.info(request, "Removed from wishlist.")
    return redirect('wishlist')


# ---- ADMIN: MANAGE WATCHES ----
@staff_member_required(login_url='login')
def admin_watch_list(request):
    watches = Watch.objects.all().order_by('-id')
    return render(request, 'watches/admin_watch_list.html', {'watches': watches})


@staff_member_required(login_url='login')
def admin_add_watch(request):
    if request.method == 'POST':
        form = WatchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Watch added successfully!")
            return redirect('admin_watch_list')
    else:
        form = WatchForm()
    return render(
        request,
        'watches/admin_watch_form.html',
        {
            'form': form,
            'action': 'Add',
        },
    )


@staff_member_required(login_url='login')
def admin_edit_watch(request, pk):
    watch = get_object_or_404(Watch, pk=pk)
    if request.method == 'POST':
        form = WatchForm(request.POST, request.FILES, instance=watch)
        if form.is_valid():
            form.save()
            messages.success(request, "Watch updated successfully!")
            return redirect('admin_watch_list')
    else:
        form = WatchForm(instance=watch)
    return render(
        request,
        'watches/admin_watch_form.html',
        {
            'form': form,
            'action': 'Edit',
            'watch': watch,
        },
    )


@staff_member_required(login_url='login')
def admin_delete_watch(request, pk):
    watch = get_object_or_404(Watch, pk=pk)
    if request.method == 'POST':
        watch.delete()
        messages.success(request, "Watch deleted successfully!")
        return redirect('admin_watch_list')
    return render(request, 'watches/admin_delete_confirm.html', {'watch': watch})
