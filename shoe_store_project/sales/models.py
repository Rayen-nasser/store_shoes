from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Sale(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        abstract = True

class NonCreditSale(Sale):
    pass

class CreditSale(Sale):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    date_of_pay = models.DateTimeField()
    has_been_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} - Credit"

@receiver(post_save, sender=NonCreditSale)
@receiver(post_save, sender=CreditSale)
def update_product_stock(sender, instance, **kwargs):
    product = instance.product
    product.stock -= instance.quantity
    product.save()
