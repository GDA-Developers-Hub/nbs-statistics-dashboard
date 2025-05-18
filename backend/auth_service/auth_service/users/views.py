from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    UserSerializer, UserDetailSerializer, UserCreateSerializer, 
    UserProfileSerializer, PasswordChangeSerializer,
    UserRegionAccessSerializer, UserSectorAccessSerializer
)
from .models import UserRegionAccess, UserSectorAccess

User = get_user_model()

class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    Permission to allow only admin and super admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            User.ROLE_ADMIN, User.ROLE_SUPER_ADMIN
        ]

class IsSuperAdminOnly(permissions.BasePermission):
    """
    Permission to allow only super admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_SUPER_ADMIN

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users.
    
    List, create, retrieve, update, and delete users based on role permissions.
    - Super Admin: Full access to all operations
    - Admin: Can create, view, and update users, but not delete
    - Analysts & Regular Users: Can only view their own profile
    - Public Users: No access
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        Define permissions based on action:
        - list, create: Admin or Super Admin
        - retrieve: Admin, Super Admin, or self
        - update, partial_update: Admin, Super Admin, or self
        - destroy: Super Admin only
        """
        if self.action in ['list', 'create']:
            permission_classes = [IsAdminOrSuperAdmin]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated]  # Further checks in has_object_permission
        elif self.action == 'destroy':
            permission_classes = [IsSuperAdminOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return UserDetailSerializer
        return UserSerializer
    
    def get_object(self):
        """
        Override to check if user is accessing their own profile.
        """
        obj = super().get_object()
        # Check if user is accessing their own profile or has admin rights
        if not (self.request.user.is_admin_user or obj.id == self.request.user.id):
            self.permission_denied(self.request)
        return obj
    
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """
        Change user password.
        Admins can change any user's password, users can only change their own.
        """
        user = self.get_object()
        serializer = PasswordChangeSerializer(data=request.data)
        
        if serializer.is_valid():
            # Admin users can change passwords without providing current password
            if not request.user.is_admin_user:
                # Regular users need to provide correct current password
                if not user.check_password(serializer.validated_data['current_password']):
                    return Response(
                        {"current_password": ["Wrong password."]}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Set new password and save
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"status": "password set"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """
        Toggle user active status. Admin or Super Admin only.
        """
        if not request.user.is_admin_user:
            return Response(
                {"detail": "You don't have permission to perform this action."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        
        return Response({
            "status": "success", 
            "is_active": user.is_active
        })
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current user's profile.
        """
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """
        Update current user's profile.
        """
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegionAccessViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user region access.
    Admin or Super Admin only.
    """
    queryset = UserRegionAccess.objects.all()
    serializer_class = UserRegionAccessSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    
    def get_queryset(self):
        """
        Filter queryset based on user_id from query params.
        """
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset

class UserSectorAccessViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user sector access.
    Admin or Super Admin only.
    """
    queryset = UserSectorAccess.objects.all()
    serializer_class = UserSectorAccessSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    
    def get_queryset(self):
        """
        Filter queryset based on user_id from query params.
        """
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset
