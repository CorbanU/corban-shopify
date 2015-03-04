from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('description', 'product_type', 'account_number')
    ordering = ('description',)
    readonly_fields = ('description', 'product_type', 'product_id')

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
