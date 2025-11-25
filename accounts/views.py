from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# ============================================
#               REGISTRO
# ============================================
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Usuario creado correctamente",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
            }, status=201)

        return Response(serializer.errors, status=400)



# ============================================
#               LOGIN
# ============================================
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Login exitoso",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
            })

        return Response(serializer.errors, status=400)



# ============================================
#   PERFIL DEL USUARIO (GET y UPDATE)
# ============================================
@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_profile(request):

    user = request.user

    # -------- GET PERFIL --------
    if request.method == "GET":
        return Response({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        })

    # -------- EDITAR PERFIL --------
    if request.method == "PUT":
        data = request.data

        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)

        new_email = data.get("email", user.email)

        # proteger el email
        if new_email != user.email:
            if User.objects.filter(email=new_email).exists():
                return Response({"error": "El email ya está en uso."}, status=400)
            user.email = new_email

        user.save()

        return Response({
            "message": "Perfil actualizado.",
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
        })



# ============================================
#   CAMBIAR CONTRASEÑA
# ============================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):

    user = request.user
    data = request.data

    current = data.get("current_password")
    new = data.get("new_password")
    new2 = data.get("new_password2")

    # validar actual
    if not check_password(current, user.password):
        return Response({"error": "La contraseña actual es incorrecta."}, status=400)

    if new != new2:
        return Response({"error": "Las contraseñas nuevas no coinciden."}, status=400)

    if len(new) < 6:
        return Response({"error": "La contraseña debe tener mínimo 6 caracteres."}, status=400)

    # guardar nueva contraseña
    user.set_password(new)
    user.save()

    return Response({"message": "Contraseña cambiada correctamente."})