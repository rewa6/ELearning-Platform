from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, EndUserAccount, ElearningModule
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import (
    CustomUserSerializer,
    CustomUserUpdateSerializer,
    EndUserAccountSerializer,
    RegisterSerializer, 
    LoginSerializer, 
    EndUserLoginSerializer,
    ModuleDetailSerializer,
    ModuleUploadSerializer,
    EndUserBriefSerializer,
    SimpleUserSerializer,
    DashboardStatsSerializer
)
from django.utils import timezone
import random
import string

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
        # if not end_user.login_timestamp:
        #     from django.utils import timezone
        #     end_user.login_timestamp = timezone.now()
        #     end_user.save()

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


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'user':
            return Response({"error": "Access denied"}, status=403)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        if user.role != 'user':
            return Response({"error": "Access denied"}, status=403)
        serializer = CustomUserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"})
        return Response(serializer.errors, status=400)

class UserEndUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'user':
            return Response({"error": "Access denied"}, status=403)
        end_users = EndUserAccount.objects.filter(parent_user=user)
        serializer = EndUserAccountSerializer(end_users, many=True)
        return Response(serializer.data)
    

class SubscriptionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'user':
            return Response({"error": "Access denied"}, status=403)

        user.profile.subscription_start = timezone.now()
        user.profile.subscription_end = timezone.now() + timezone.timedelta(days=30)
        user.profile.subscription_active = True
        user.profile.save()

        return Response({"message": "Subscription activated"})


class SubscriptionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'user':
            return Response({"error": "Access denied"}, status=403)

        profile = user.profile
        data = {
            "active": profile.subscription_active,
            "start": profile.subscription_start,
            "end": profile.subscription_end
        }
        return Response(data)


class SubscriptionRenewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'user':
            return Response({"error": "Access denied"}, status=403)

        profile = user.profile
        if profile.subscription_end:
            profile.subscription_end += timezone.timedelta(days=30)
        else:
            profile.subscription_start = timezone.now()
            profile.subscription_end = timezone.now() + timezone.timedelta(days=30)
        profile.subscription_active = True
        profile.save()

        return Response({"message": "Subscription renewed"})


class SubscriptionReminderEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'user':
            return Response({"error": "Access denied"}, status=403)

        # Simulate sending email
        print(f"Sending reminder to {user.email}")  # Replace with send_mail() or Celery task

        return Response({"message": "Reminder email sent"})

class EndUserGenerateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'user':
            return Response({"error": "Access denied"}, status=403)

        end_users = []
        for _ in range(10):
            login_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            end_user = EndUserAccount.objects.create(
                parent_user=user,
                login_id=login_id,
                password=password,
                is_active=True
            )
            end_users.append(end_user)

        serializer = EndUserAccountSerializer(end_users, many=True)
        return Response({
            "message": "10 end-user accounts created",
            "accounts": serializer.data
        })


class EndUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return Response({"error": "Access denied"}, status=403)
        end_users = EndUserAccount.objects.filter(parent_user=user)
        serializer = EndUserAccountSerializer(end_users, many=True)
        return Response(serializer.data)

class EndUserDeactivateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        user = request.user
        if user.role != 'user':
            return Response({"error": "Access denied"}, status=403)

        try:
            end_user = EndUserAccount.objects.get(id=id, parent_user=user)
        except EndUserAccount.DoesNotExist:
            return Response({"error": "End-user not found"}, status=404)

        end_user.is_active = False
        end_user.save()
        return Response({"message": f"End-user {end_user.login_id} deactivated"})


class EndUserValidateView(APIView):
    def post(self, request):
        login_id = request.data.get("login_id")
        if not login_id:
            return Response({"error": "login_id required"}, status=400)

        try:
            account = EndUserAccount.objects.get(login_id=login_id)
        except EndUserAccount.DoesNotExist:
            return Response({"valid": False, "message": "Login ID not found"})

        if not account.is_active:
            return Response({"valid": False, "message": "Account is inactive or expired"})

        return Response({
            "valid": True,
            "login_id": account.login_id,
            "expires_on": account.expiration_timestamp
        })

class ModuleUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role not in ['admin', 'user']:
            return Response({"error": "Unauthorized"}, status=403)

        serializer = ModuleUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=user)
            return Response({"message": "Module uploaded successfully", "module": serializer.data})
        return Response(serializer.errors, status=400)


class ModulePublishToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            module = ElearningModule.objects.get(id=id, uploaded_by=request.user)
        except ElearningModule.DoesNotExist:
            return Response({"error": "Module not found or not owned"}, status=404)

        module.publish = not module.publish
        module.save()
        return Response({
            "message": f"Module {'published' if module.publish else 'unpublished'}",
            "publish": module.publish
        })


class ModuleListView(APIView):
    def get(self, request):
        modules = ElearningModule.objects.filter(publish=True).order_by('-created_at')
        serializer = ModuleUploadSerializer(modules, many=True)
        return Response(serializer.data)


class ModuleDetailView(APIView):
    def get(self, request, id):
        try:
            module = ElearningModule.objects.get(id=id, publish=True)
        except ElearningModule.DoesNotExist:
            return Response({"error": "Module not found"}, status=404)

        serializer = ModuleDetailSerializer(module)
        return Response(serializer.data)


class ModuleLaunchView(APIView):
    def get(self, request, id):
        try:
            module = ElearningModule.objects.get(id=id, publish=True)
        except ElearningModule.DoesNotExist:
            return Response({"error": "Module not found"}, status=404)

        # You can adapt this URL pattern based on how you serve static files
        zip_url = module.zip_file.url
        return Response({
            "message": "Launch module",
            "launch_url": zip_url  # Or route to a viewer frontend
        })

class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'user':
            return Response({"error": "Access denied"}, status=403)

        total_modules = ElearningModule.objects.filter(uploaded_by=user).count()
        total_end_users = EndUserAccount.objects.filter(parent_user=user).count()
        active = EndUserAccount.objects.filter(parent_user=user, is_active=True).count()
        expired = total_end_users - active

        stats = {
            'total_modules': total_modules,
            'total_end_users': total_end_users,
            'active_end_users': active,
            'expired_end_users': expired
        }
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)

class UserCertificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Placeholder: assume certifications later
        return Response({
            "certifications": []
        })

# ------------------ ADMIN DASHBOARD ------------------ #

class AdminUsersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({"error": "Access denied"}, status=403)

        users = CustomUser.objects.filter(role='user')
        serializer = SimpleUserSerializer(users, many=True)
        return Response(serializer.data)

class AdminEndUsersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({"error": "Access denied"}, status=403)

        end_users = EndUserAccount.objects.all()
        serializer = EndUserBriefSerializer(end_users, many=True)
        return Response(serializer.data)

class AdminExpiringSoonView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({"error": "Access denied"}, status=403)

        threshold = timezone.now() + timezone.timedelta(days=5)
        expiring = EndUserAccount.objects.filter(
            is_active=True,
            expiration_timestamp__lt=threshold
        ).order_by('expiration_timestamp')

        serializer = EndUserBriefSerializer(expiring, many=True)
        return Response(serializer.data)

# class SupportContactView(APIView):
#     def post(self, request):
#         return Response({"message": "Support contact form"})

# class HelpFAQView(APIView):
#     def get(self, request):
#         return Response({"message": "Help/FAQ"})

# class AboutPlatformView(APIView):
#     def get(self, request):
#         return Response({"message": "About the platform"})
