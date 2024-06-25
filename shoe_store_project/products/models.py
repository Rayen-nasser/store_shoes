from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
class Size(models.Model):
    size = models.CharField(max_length=3)

    def __str__(self):
        return self.size

class Color(models.Model):
    color = models.CharField(max_length=30)
    hex_code = models.CharField(max_length=6, default='000000')  # Example default value

    def __str__(self):
        return self.color


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class GenerationCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/photos/%Y/%m/%d')
    image_1 = models.ImageField(upload_to='products/photos/%Y/%m/%d', blank=True, null=True)
    image_2 = models.ImageField(upload_to='products/photos/%Y/%m/%d', blank=True, null=True)
    image_3 = models.ImageField(upload_to='products/photos/%Y/%m/%d', blank=True, null=True)
    sizes = models.ManyToManyField(Size)
    colors = models.ManyToManyField(Color)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True, blank=True)
    generation_category = models.ForeignKey(GenerationCategory, on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)  # Rating score
    comment = models.TextField(blank=True, null=True)  # Optional comment
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # Ensure a user can rate a product only once

    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.score}'