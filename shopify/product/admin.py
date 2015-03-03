from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('description', 'product_type', 'account_number')

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
