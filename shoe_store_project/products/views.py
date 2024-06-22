from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Season, Color, Size


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

def get_search_options():
    categories = Category.objects.all()
    seasons = Season.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()
    return categories, seasons, colors, sizes

def search(request):
    # Retrieve available search options
    categories = Category.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()
    seasons = Season.objects.all()

    # Retrieve the selected filters from the query parameters
    query_params = request.GET
    selected_filters = {
        'category': query_params.getlist('category'),
        'size': query_params.getlist('size'),
        'color': query_params.getlist('color'),
        'season': query_params.getlist('season'),
    }

    # Convert color names to corresponding Color objects
    selected_filters['color_objects'] = Color.objects.filter(color__in=selected_filters['color'])

    # Filter products based on selected filters
    filtered_products = Product.objects.all()
    if selected_filters['category']:
        filtered_products = filtered_products.filter(category__name__in=selected_filters['category'])
    if selected_filters['size']:
        # Instead of using distinct(), we can use the distinct() method after the filtering process
        filtered_products = filtered_products.filter(sizes__size__in=selected_filters['size'])
    if selected_filters['color_objects']:
        filtered_products = filtered_products.filter(colors__in=selected_filters['color_objects'])
    if selected_filters['season']:
        filtered_products = filtered_products.filter(season__name__in=selected_filters['season'])

    # Use distinct() to remove duplicate products after applying all filters
    filtered_products = filtered_products.distinct()

    context = {
        'products': filtered_products,
        'selected_filters': selected_filters,
        'categories': categories,
        'sizes': sizes,
        'colors': colors,
        'seasons': seasons,
    }
    return render(request, 'products/search.html', context)


