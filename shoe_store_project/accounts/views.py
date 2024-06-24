from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate

from .models import SaveFavorite
from products.models import Product


@login_required
def favorite_products(request):
    favorites = SaveFavorite.objects.filter(user=request.user).select_related('product')
    context = {'favorites': favorites}
    return render(request, 'products/favorite_products.html', context)


@login_required
def save_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = SaveFavorite.objects.get_or_create(user=request.user, product=product)

    if not created:
        # If the favorite already exists, delete it (toggle)
        favorite.delete()
        messages.success(request, 'Product removed from favorites.')
    else:
        messages.success(request, 'Product saved to favorites.')

    # Redirect back to the previous page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_protect
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You are logged in.')
                return redirect('favorite_products')
            else:
                messages.error(request, 'Invalid login credentials.')
        else:
            messages.error(request, 'Please provide both email and password.')

        return redirect('login')

    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
                return redirect('register')
            else:
                # Create user
                user = User.objects.create_user( username=username,
                                                email=email,
                                                 password=password)

                # Log in the user after successful registration
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, user)

                messages.success(request, 'You are registered successfully.')
                return redirect('home')  # Redirect to dashboard after successful registration and login
        else:
            messages.error(request, "Passwords don't match")
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def logout(request):
    if request.method == 'POST':
        print("logout")
        auth.logout(request)
        # messages.success(request, 'You are successfully logged out.')
        return redirect('home')
    return redirect('home')
