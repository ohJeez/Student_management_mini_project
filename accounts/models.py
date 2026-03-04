from django.db import models
from django.contrib.auth.models import User


class ROLES:
    ADMIN = 'admin'
    STAFF = 'staff'
    VIEWER = 'viewer'

    CHOICES = [
        (ADMIN,  'Admin'),
        (STAFF,  'Staff / Teacher'),
        (VIEWER, 'Viewer'),
    ]


class UserProfile(models.Model):
    """One-to-one extension of the built-in User model that adds a role."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(
        max_length=20,
        choices=ROLES.CHOICES,
        default=ROLES.VIEWER,
    )

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    # ── convenience helpers ────────────────────────────────────────────────
    def is_admin(self):
        return self.role == ROLES.ADMIN

    def is_staff_role(self):
        return self.role == ROLES.STAFF

    def is_viewer(self):
        return self.role == ROLES.VIEWER

    def can_edit(self):
        """Admin and Staff may create/update students."""
        return self.role in (ROLES.ADMIN, ROLES.STAFF)

    def can_delete(self):
        """Only Admin may delete students."""
        return self.role == ROLES.ADMIN

    def can_manage_users(self):
        """Only Admin may manage the user list."""
        return self.role == ROLES.ADMIN
