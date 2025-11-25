from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegionViewSet, ProvinceViewSet, CommuneViewSet, AddressViewSet

router = DefaultRouter()
router.register(r"regions", RegionViewSet, basename="region")
router.register(r"provinces", ProvinceViewSet, basename="province")
router.register(r"communes", CommuneViewSet, basename="commune")
router.register(r"addresses", AddressViewSet, basename="address")

urlpatterns = [
    path("", include(router.urls)),
]