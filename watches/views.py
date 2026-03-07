from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import Watch,Cart
from .forms import CustomerRegistrationForm, LoginForm

from .forms import AddressForm
from .models import Address
from .forms import EditProfileForm


# ---------------- HOME ----------------
def home(request):
    return render(request, 'watches/home.html')


# ---------------- ABOUT ----------------
def about(request):
    return render(request, 'watches/about.html')


# ---------------- CONTACT ----------------
def contact(request):
    return render(request, 'watches/contact.html')


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
    return render(request, "watches/profile.html")

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

    context = {
        'cart_items': cart_items,
        'addresses': addresses,
        'total': total
    }

    return render(request, 'watches/checkout.html', context)