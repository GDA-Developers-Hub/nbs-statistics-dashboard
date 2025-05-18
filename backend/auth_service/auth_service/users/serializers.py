from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserRegionAccess, UserSectorAccess
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that adds user role to the token
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['role'] = user.role
        token['email'] = user.email
        token['full_name'] = user.full_name
        
        return token

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with basic information.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'is_active', 'language_preference']
        read_only_fields = ['id']

class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for User model with all fields.
    """
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'role', 'organization',
            'position', 'phone_number', 'language_preference',
            'is_active', 'two_factor_enabled', 'date_joined',
            'last_login', 'last_password_change'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'last_password_change']

class UserRegionAccessSerializer(serializers.ModelSerializer):
    """
    Serializer for UserRegionAccess model.
    """
    class Meta:
        model = UserRegionAccess
        fields = ['id', 'user', 'region_code', 'access_level', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserSectorAccessSerializer(serializers.ModelSerializer):
    """
    Serializer for UserSectorAccess model.
    """
    class Meta:
        model = UserSectorAccess
        fields = ['id', 'user', 'sector_code', 'access_level', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user with password validation.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password2', 'full_name', 'role',
            'organization', 'position', 'phone_number', 'language_preference'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile information.
    """
    class Meta:
        model = User
        fields = [
            'full_name', 'organization', 'position',
            'phone_number', 'language_preference'
        ]
