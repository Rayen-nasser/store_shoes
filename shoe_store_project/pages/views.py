from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

from pages.models import Subscribe
from django.contrib import messages

def home(request):
    if request.method == 'POST':
        email = request.POST.get('subscribe')
        if email:
            # Save the email to the database
            Subscribe.objects.create(email=email)
            return redirect('home')  # Redirect to home to avoid re-submission on refresh
        else:
            return HttpResponse("Invalid email input", status=400)
    return render(request, 'pages/home.html')

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