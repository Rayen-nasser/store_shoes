from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Season, Color, Size, GenerationCategory, Review, ReviewVote
from accounts.models import SaveFavorite
from django.contrib import messages

def products(request):
    products_list = Product.objects.order_by('-created_date')
    keyword = request.GET.get('keyword')
    if keyword:
        products_list = products_list.filter(
            Q(name__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(category__name__icontains=keyword) |
            Q(season__name__icontains=keyword) |
            Q(generation_category__name__icontains=keyword) |
            Q(sizes__size__icontains=keyword) |
            Q(colors__color__icontains=keyword)
        ).distinct()  # distinct() to avoid duplicates due to many-to-many relationships

    if request.user.is_authenticated:
        # Get the list of product IDs that are favorites for the authenticated user
        favorite_product_ids = SaveFavorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        favorite_product_ids = []

        # Annotate each product with whether it is a favorite for the authenticated user
    for product in products_list:
        product.is_favorite = product.id in favorite_product_ids

    paginator = Paginator(products_list, 6)  # Show 8 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'keyword': keyword,
    }
    return render(request, 'products/products.html', context)


@login_required
def vote_review(request, pk):
    review = get_object_or_404(Review, id=pk)
    like = request.POST.get('action') == 'like'

    # Check if the user has already voted on this review
    review_vote, created = ReviewVote.objects.get_or_create(review=review, user=request.user, defaults={'like': like})

    if not created:
        if review_vote.like != like:
            review_vote.like = like
            review_vote.save()

    return redirect('product_details', pk=review.product.pk)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)

    total_score = sum(review.score for review in reviews)
    review_count = reviews.count()
    avg_rating = total_score // review_count if review_count > 0 else 0

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = SaveFavorite.objects.filter(user=request.user, product=product).exists()

    for review in reviews:
        review.num_likes = review.votes.filter(like=True).count()
        review.num_dislikes = review.votes.filter(like=False).count()

        review.has_voted = False
        if not isinstance(request.user, AnonymousUser):
            user_vote = review.votes.filter(user=request.user).first()
            if user_vote:
                review.has_voted = True
                review.user_vote = user_vote

    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    return render(request, 'products/product_details.html', {
        'product': product,
        'reviews': reviews,
        'is_favorite': is_favorite,
        'avg_rating': avg_rating,
        'user_review': user_review,
    })

@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            # Check if the user has already reviewed this product
            existing_review = Review.objects.filter(product=product, user=request.user).exists()
            if existing_review:
                # If the user has already reviewed this product, update the existing review
                review = Review.objects.get(product=product, user=request.user)
                review.score = rating
                review.comment = comment
                review.save()
            else:
                # If the user has not reviewed this product yet, create a new review
                review = Review.objects.create(
                    product=product,
                    user=request.user,
                    score=rating,
                    comment=comment
                )
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('product_details', pk=product.pk)

    # Redirect back to the product detail page if the request method is not POST
    return redirect('product_details', pk=product.pk)
@login_required
def update_review(request, product_id, review_id):
    product = get_object_or_404(Product, id=product_id)
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            review.score = rating
            review.comment = comment
            review.save()
            messages.success(request, 'Your review has been updated successfully!')
            return redirect('product_details', pk=product.pk)

    context = {
        'product': product,
        'review': review
    }
    return render(request, 'update_review.html', context)

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
    generations = GenerationCategory.objects.all()

    # Retrieve the selected filters from the query parameters
    query_params = request.GET
    selected_filters = {
        'category': query_params.getlist('category'),
        'size': query_params.getlist('size'),
        'color': query_params.getlist('color'),
        'season': query_params.getlist('season'),
        'generation': query_params.getlist('generation'),
        'sort': query_params.getlist('sort'),
    }

    # Filter products based on selected filters
    filtered_products = Product.objects.all()

    if selected_filters['category']:
        filtered_products = filtered_products.filter(category__name__in=selected_filters['category'])
    if selected_filters['generation']:
        filtered_products = filtered_products.filter(generation_category__name__in=selected_filters['generation'])
    if selected_filters['size']:
        filtered_products = filtered_products.filter(sizes__size__in=selected_filters['size'])
    if selected_filters['color']:
        filtered_products = filtered_products.filter(colors__color__in=selected_filters['color'])
    if selected_filters['season']:
        filtered_products = filtered_products.filter(season__name__in=selected_filters['season'])

    # Handle sorting
    sort_method = query_params.get('sort')
    if selected_filters['sort']:
        if sort_method == "most_popular":
            filtered_products = filtered_products.annotate(review_count=Count('ratings')).order_by('-review_count')
        elif sort_method == "best_rating":
            filtered_products = filtered_products.annotate(average_rating=Avg('ratings__score')).order_by(
                '-average_rating')
        elif sort_method == "newest":
            filtered_products = filtered_products.order_by('-created_date')
        elif sort_method == "price_low_high":
            filtered_products = filtered_products.order_by('price')
        elif sort_method == "price_high_low":
            filtered_products = filtered_products.order_by('-price')

    # Use distinct() to remove duplicate products after applying all filters
    filtered_products = filtered_products.distinct()

    # Annotate each product with whether it is a favorite for the authenticated user
    favorite_product_ids = []
    if request.user.is_authenticated:
        favorite_product_ids = SaveFavorite.objects.filter(user=request.user).values_list('product_id', flat=True)

    for product in filtered_products:
        product.is_favorite = product.id in favorite_product_ids

    context = {
        'products': filtered_products,
        'selected_filters': selected_filters,
        'categories': categories,
        'sizes': sizes,
        'colors': colors,
        'seasons': seasons,
        'generations': generations,
        'sort_method': sort_method,
    }

    return render(request, 'products/search.html', context)