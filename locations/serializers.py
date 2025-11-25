from rest_framework import serializers
from .models import Region, Province, Commune, Address


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "code", "name"]


class ProvinceSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Province
        fields = ["id", "code", "name", "region"]


class CommuneSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)

    class Meta:
        model = Commune
        fields = ["id", "code", "name", "province"]


class AddressSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    province = ProvinceSerializer(read_only=True)
    commune = CommuneSerializer(read_only=True)

    region_id = serializers.PrimaryKeyRelatedField(
        source="region",
        queryset=Region.objects.all(),
        write_only=True,
    )
    province_id = serializers.PrimaryKeyRelatedField(
        source="province",
        queryset=Province.objects.all(),
        write_only=True,
    )
    commune_id = serializers.PrimaryKeyRelatedField(
        source="commune",
        queryset=Commune.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Address
        fields = [
            "id",
            "street",
            "number",
            "apartment",
            "reference",
            "postal_code",
            "is_default",
            "region",
            "province",
            "commune",
            "region_id",
            "province_id",
            "commune_id",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        # si marca esta como default, desmarcamos las otras
        if validated_data.get("is_default", False):
            Address.objects.filter(user=user, is_default=True).update(is_default=False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("is_default", False):
            Address.objects.filter(user=instance.user, is_default=True).exclude(
                pk=instance.pk
            ).update(is_default=False)
        return super().update(instance, validated_data)