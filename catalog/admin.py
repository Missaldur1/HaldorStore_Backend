from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "currency", "stock", "featured")
    list_filter = ("category", "featured", "currency")
    search_fields = ("name", "slug", "description", "tags")
    prepopulated_fields = {"slug": ("name",)}