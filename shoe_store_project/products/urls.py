from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name="products"),
    path('<int:pk>/', views.product_detail, name="product_details"),  # Changed 'id' to 'pk'
    path('search/', views.search, name="search"),
    path('<int:product_id>/add_review/', views.add_review, name='add_review'),
]
