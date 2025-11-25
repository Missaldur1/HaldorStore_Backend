from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Region(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Región"
        verbose_name_plural = "Regiones"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Province(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=150)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="provinces",
    )

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Commune(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=150)
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name="communes",
    )

    class Meta:
        verbose_name = "Comuna"
        verbose_name_plural = "Comunas"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Address(models.Model):
    """
    Dirección de usuario (después la podremos asociar a pedidos).
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="addresses")
    province = models.ForeignKey(Province, on_delete=models.PROTECT, related_name="addresses")
    commune = models.ForeignKey(Commune, on_delete=models.PROTECT, related_name="addresses")

    street = models.CharField("Calle / Avenida", max_length=255)
    number = models.CharField("Número", max_length=20, blank=True)
    apartment = models.CharField("Depto / Casa / Otro", max_length=50, blank=True)
    reference = models.CharField("Referencia", max_length=255, blank=True)
    postal_code = models.CharField("Código postal", max_length=20, blank=True)

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        ordering = ["-is_default", "-created_at"]

    def __str__(self):
        base = f"{self.street} {self.number}".strip()
        return f"{base}, {self.commune.name}, {self.region.name}"