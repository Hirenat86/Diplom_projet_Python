from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from .models import Category, Product, ProductInfo, ProductParameter, Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    model = Shop
    list_display = ["id", "name", "user"]
    list_editable = ["name", "user"]


class ProductParameterInline(NestedStackedInline):
    model = ProductParameter


class ProductInfoInline(NestedStackedInline):
    model = ProductInfo
    inlines = [ProductParameterInline]


class ProductAdmin(NestedModelAdmin):
    model = Product
    list_display = ["id", "name", "category"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductInfoInline]


admin.site.register(Product, ProductAdmin)
