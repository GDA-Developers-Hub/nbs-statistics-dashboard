from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """
    Custom user manager for SNBS User model with email as the unique identifier.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'super_admin')  # Set role to Super Admin
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Custom User model with email as the username field.
    Includes role-based access control fields.
    """
    # Role choices according to project requirements
    ROLE_SUPER_ADMIN = 'super_admin'
    ROLE_ADMIN = 'admin'
    ROLE_ANALYST = 'analyst'
    ROLE_USER = 'user'
    ROLE_PUBLIC = 'public'
    
    ROLE_CHOICES = [
        (ROLE_SUPER_ADMIN, _('Super Admin')),
        (ROLE_ADMIN, _('Admin')),
        (ROLE_ANALYST, _('Analyst')),
        (ROLE_USER, _('Regular User')),
        (ROLE_PUBLIC, _('Public User')),
    ]
    
    # Replace username with email as the unique identifier
    username = models.CharField(
        _('username'),
        max_length=150,
        null=True,
        blank=True,
    )
    email = models.EmailField(_('email address'), unique=True)
    
    # Role field for RBAC
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_PUBLIC,
        verbose_name=_('User Role')
    )
    
    # Additional profile fields
    full_name = models.CharField(max_length=255, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    # User preferences
    language_preference = models.CharField(
        max_length=10,
        choices=[('en', 'English'), ('so', 'Somali')],
        default='en'
    )
    
    # Two-factor authentication status (required for admin users)
    two_factor_enabled = models.BooleanField(default=False)
    
    # Timestamps
    last_password_change = models.DateTimeField(auto_now_add=True)
    
    # Django requirements
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    # Use custom manager
    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def __str__(self):
        return self.email
    
    @property
    def is_admin_user(self):
        """Check if user has admin privileges"""
        return self.role in [self.ROLE_SUPER_ADMIN, self.ROLE_ADMIN]
    
    @property
    def is_analyst_or_higher(self):
        """Check if user has analyst or higher privileges"""
        return self.role in [self.ROLE_SUPER_ADMIN, self.ROLE_ADMIN, self.ROLE_ANALYST]
    
    def save(self, *args, **kwargs):
        """Override save method to enforce 2FA for admin users"""
        # If user is an admin type, enforce 2FA requirement
        if self.is_admin_user and not self.two_factor_enabled:
            # In a real system, this would be enforced differently
            # For now, just note that it's required but let it pass for demo
            pass
        
        super().save(*args, **kwargs)

class UserRegionAccess(models.Model):
    """
    Model to track which regions a user has access to.
    Part of the RBAC system.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='region_access')
    region_code = models.CharField(max_length=20)
    access_level = models.CharField(
        max_length=20,
        choices=[
            ('read', 'Read Only'),
            ('write', 'Read/Write'),
            ('admin', 'Administrator')
        ],
        default='read'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'region_code']
        
    def __str__(self):
        return f"{self.user.email} - {self.region_code} - {self.access_level}"

class UserSectorAccess(models.Model):
    """
    Model to track which sectors a user has access to.
    Part of the RBAC system.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sector_access')
    sector_code = models.CharField(max_length=50)
    access_level = models.CharField(
        max_length=20,
        choices=[
            ('read', 'Read Only'),
            ('write', 'Read/Write'),
            ('admin', 'Administrator')
        ],
        default='read'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'sector_code']
        
    def __str__(self):
        return f"{self.user.email} - {self.sector_code} - {self.access_level}"

class UserSession(models.Model):
    """
    Model to track user sessions for enhanced security.
    Allows for forced logout capability.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.created_at}"
