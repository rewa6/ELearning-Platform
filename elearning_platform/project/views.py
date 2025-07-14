from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, EndUserAccount
from .serializers import RegisterSerializer, LoginSerializer, EndUserLoginSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User registered successfully",
            "user_id": user.id
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": user.role
        })


class EndUserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = EndUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        login_id = serializer.validated_data['login_id']
        password = serializer.validated_data['password']

        try:
            end_user = EndUserAccount.objects.get(login_id=login_id)
        except EndUserAccount.DoesNotExist:
            return Response({"error": "Invalid Login ID"}, status=404)

        if not end_user.is_active:
            return Response({"error": "Account expired or inactive"}, status=403)

        if end_user.password != password:
            return Response({"error": "Incorrect password"}, status=401)

        # Optional: track first login
        if not end_user.login_timestamp:
            from django.utils import timezone
            end_user.login_timestamp = timezone.now()
            end_user.save()

        return Response({
            "message": "End user authenticated",
            "login_id": end_user.login_id
        })


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
