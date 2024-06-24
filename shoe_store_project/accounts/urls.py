from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('favorite_products/', views.favorite_products, name='favorite_products'),
    path('save_favorite/<int:product_id>/', views.save_favorite, name='save_favorite'),
]