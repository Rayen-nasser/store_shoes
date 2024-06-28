from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from pages.models import Subscribe
from django.contrib import messages

from products.models import Product
from accounts.models import SaveFavorite

def home(request):
    products_list = Product.objects.order_by('-created_date')
    paginator = Paginator(products_list, 6)  # Show 8 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        # Get the list of product IDs that are favorites for the authenticated user
        favorite_product_ids = SaveFavorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        favorite_product_ids = []

    # Annotate each product with whether it is a favorite for the authenticated user
    for product in page_obj:
        product.is_favorite = product.id in favorite_product_ids

    context = {
        'page_obj': page_obj,
    }

    if request.method == 'POST':
        email = request.POST.get('subscribe')
        if email:
            # Save the email to the database
            Subscribe.objects.create(email=email)
            return redirect('home')  # Redirect to home to avoid re-submission on refresh
        else:
            return HttpResponse("Invalid email input", status=400)

    return render(request, 'pages/home.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send email to admin
        send_mail(
            f'Contact Form Submission: {subject}',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        # Add success message
        messages.success(request, 'Your message has been sent successfully!')

        # Redirect to home page
        return redirect('home')

    return render(request, 'pages/contact.html')

def about(request):
    return render(request, 'pages/about.html')

def services(request):
    return render(request, 'pages/services.html')

