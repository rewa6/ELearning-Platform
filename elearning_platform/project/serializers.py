from rest_framework import serializers
from .models import CustomUser, EndUserAccount, UserProfile, ElearningModule

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class EndUserLoginSerializer(serializers.Serializer):
    login_id = serializers.CharField()
    password = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['subscription_start', 'subscription_end', 'subscription_active', 'total_end_users']

class EndUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUserAccount
        fields = ['login_id', 'is_active', 'login_timestamp', 'expiration_timestamp']

class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'role',
            'profile_image',
            'profile'
        ]

class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'profile_image']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['subscription_start', 'subscription_end', 'subscription_active', 'total_end_users']

class EndUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUserAccount
        fields = ['login_id', 'is_active', 'login_timestamp', 'expiration_timestamp']


class ModuleUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElearningModule
        fields = [
            'id', 'title', 'description', 'thumbnail', 'zip_file', 'publish', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'uploaded_by']

class ModuleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElearningModule
        fields = '__all__'

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']

class DashboardStatsSerializer(serializers.Serializer):
    total_modules = serializers.IntegerField()
    total_end_users = serializers.IntegerField()
    active_end_users = serializers.IntegerField()
    expired_end_users = serializers.IntegerField()

class EndUserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUserAccount
        fields = ['login_id', 'is_active', 'expiration_timestamp']