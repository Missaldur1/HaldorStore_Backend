from django.db import models
from django.utils.text import slugify

CURRENCY_CHOICES = [
    ("CLP", "Peso chileno"),
    ("USD", "Dólar estadounidense"),
]

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
        help_text="Imagen representativa de esta categoría (se usa en el Home)."
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    # Campos principales
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="CLP")

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        help_text="Imagen principal del producto",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    stock = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3, decimal_places=1, blank=True, null=True, help_text="Ej: 4.7"
    )

    featured = models.BooleanField(default=False)
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Tags separados por coma, ej: invierno,runas,barco",
    )

    description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    material = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)
    origin = models.CharField(max_length=100, blank=True)

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def tags_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(",") if t.strip()]