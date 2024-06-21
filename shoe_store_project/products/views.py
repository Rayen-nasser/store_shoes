from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Product

def products(request):
    product_list = Product.objects.order_by('-created_date')
    paginator = Paginator(product_list, 10)  # Show 10 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'products/products.html', context)

def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    context = {
        'product': product
    }
    return render(request, 'products/product_details.html', context)