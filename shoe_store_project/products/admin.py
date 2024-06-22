from django.contrib import admin
from .models import Product, Size, Color, Category, Season, GenerationCategory

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'price', 'stock', 'category', 'season']
    list_filter = ['category', 'season']
    search_fields = ['name', 'description']
    filter_horizontal = ['sizes', 'colors']
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        return '<img src="%s" width="100" />' % obj.image.url

    image_tag.allow_tags = True

admin.site.register(Product, ProductAdmin)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Category)
admin.site.register(Season)
admin.site.register(GenerationCategory)
