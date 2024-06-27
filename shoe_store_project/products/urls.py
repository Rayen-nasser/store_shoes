from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name="products"),
    path('search/', views.search, name="search"),
    path('<int:pk>/', views.product_detail, name="product_details"),
    path('<int:pk>/add_review/', views.add_review, name='add_review'),
    path('<int:pk>/vote_review/', views.vote_review, name='vote_review'),
    path('product/<int:product_id>/update_review/<int:review_id>/', views.update_review, name='update_review'),
]
