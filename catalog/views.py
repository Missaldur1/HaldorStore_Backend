from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


# -----------------------
# CATEGORÍAS
# -----------------------
class CategoryListView(APIView):
    def get(self, request):
        cats = Category.objects.all()
        serializer = CategorySerializer(cats, many=True)
        return Response(serializer.data)


# -----------------------
# PRODUCTOS - LISTADO
# -----------------------
class ProductListView(APIView):
    def get(self, request):
        queryset = Product.objects.all()

        # Filtro: ?category=ropa
        category_slug = request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filtro: ?featured=1
        if request.GET.get("featured") == "1":
            queryset = queryset.filter(featured=True)

        # Filtro: ?search=hoodie
        search = request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(tags__icontains=search)
            )

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


# -----------------------
# DETALLE POR SLUG
# -----------------------
class ProductDetailView(APIView):
    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response({"detail": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data)