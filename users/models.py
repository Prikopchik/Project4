from django.conf import settings
from django.contrib.auth.models import AbstractUser,Group, Permission 
from django.db import models
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('manager', 'Менеджер'),
    ]

    email = models.EmailField(unique=True)
    is_manager = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    sent_messages = models.PositiveIntegerField(default=0)
    failed_messages = models.PositiveIntegerField(default=0)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups', 
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions', 
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def has_perm(self, perm, obj=None):
        if self.is_manager:
            return True
        return super().has_perm(perm, obj)
    
    def has_perm(self, perm, obj=None):
        if self.is_manager:
            return True
        return super().has_perm(perm, obj)
    
    def __str__(self):
        return self.username
    
class EmailConfirmationToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Токен для {self.user.username}"
