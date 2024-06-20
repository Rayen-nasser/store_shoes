from django.contrib import admin
from .models import NonCreditSale, CreditSale

class NonCreditSaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'sale_date']
    list_filter = ['product', 'sale_date']
    search_fields = ['product__name', 'quantity']

class CreditSaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'first_name', 'last_name', 'phone_number', 'date_of_pay']
    list_filter = ['product', 'date_of_pay']  # Add this line
    search_fields = ['product__name', 'quantity', 'first_name', 'last_name', 'phone_number']  # Add this line

admin.site.register(NonCreditSale, NonCreditSaleAdmin)
admin.site.register(CreditSale, CreditSaleAdmin)
