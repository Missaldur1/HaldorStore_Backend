from rest_framework import viewsets, permissions
from .models import Region, Province, Commune, Address
from .serializers import (
    RegionSerializer,
    ProvinceSerializer,
    CommuneSerializer,
    AddressSerializer,
)


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.AllowAny]


class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProvinceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Province.objects.select_related("region")
        region_id = self.request.query_params.get("region")
        if region_id:
            qs = qs.filter(region_id=region_id)
        return qs


class CommuneViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommuneSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Commune.objects.select_related("province", "province__region")
        province_id = self.request.query_params.get("province")
        region_id = self.request.query_params.get("region")
        if province_id:
            qs = qs.filter(province_id=province_id)
        if region_id:
            qs = qs.filter(province__region_id=region_id)
        return qs


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user).select_related(
            "region", "province", "commune"
        )