from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import UserProfile, ROLES


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Automatically create a UserProfile whenever a new User is saved.
    The very first user ever created (pk=1 or superuser) gets 'admin' role.
    """
    if created:
        role = ROLES.ADMIN if instance.is_superuser else ROLES.VIEWER
        UserProfile.objects.get_or_create(user=instance, defaults={'role': role})
    else:
        # Make sure profile always exists (safety net)
        UserProfile.objects.get_or_create(user=instance)
