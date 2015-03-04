from django.contrib import admin

from .models import Product
from notification.models import ProductNotification


class ProductNotificationInline(admin.TabularInline):
    max_num = 1
    model = ProductNotification


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductNotificationInline]
    list_display = ('description', 'product_type', 'account_number')
    ordering = ('description',)
    readonly_fields = ('description', 'product_type', 'product_id')

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
