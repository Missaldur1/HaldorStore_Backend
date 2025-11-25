from django.contrib import admin
from .models import Region, Province, Commune, Address


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "region")
    list_filter = ("region",)
    search_fields = ("code", "name")


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "province", "get_region")
    list_filter = ("province__region", "province")
    search_fields = ("code", "name")

    @admin.display(description="Región")
    def get_region(self, obj):
        return obj.province.region


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "street", "number", "commune", "is_default", "created_at")
    list_filter = ("is_default", "commune__province__region")
    search_fields = (
        "street",
        "number",
        "apartment",
        "user__email",
        "user__username",
    )