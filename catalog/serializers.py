from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "image"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = serializers.SerializerMethodField()
    image = serializers.ImageField(read_only=True)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "slug",
            "name",
            "price",
            "currency",
            "image",
            "category",
            "stock",
            "rating",
            "featured",
            "tags",
            # opcionales
            "description",
            "long_description",
            "material",
            "color",
            "origin",
        ]

    def get_tags(self, obj):
        if not obj.tags:
            return []
        return [t.strip() for t in obj.tags.split(",") if t.strip()]
