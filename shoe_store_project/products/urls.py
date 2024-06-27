from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name="products"),
    path('search/', views.search, name="search"),
    path('<int:pk>/', views.product_detail, name="product_details"),
    path('<int:pk>/add_review/', views.add_review, name='add_review'),
    path('<int:pk>/vote_review/', views.vote_review, name='vote_review'),
]
