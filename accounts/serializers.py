from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

# ------- REGISTRO -------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "password2", "first_name", "last_name"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden"})
        return data

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]

        # capitalizar
        first_name = validated_data["first_name"].strip().capitalize()
        last_name = validated_data["last_name"].strip().capitalize()

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user


# ------- LOGIN -------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # autenticación basada en EMAIL
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Credenciales inválidas")

        data["user"] = user
        return data
