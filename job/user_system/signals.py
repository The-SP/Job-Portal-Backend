from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserAccount, Profile
from resume.models import Resume


@receiver(post_save, sender=UserAccount)
def create_profile_resume(sender, instance, created, **kwargs):
    """
    Signal to create profile and resume when Seeker user is created
    """
    if created and not instance.is_employer:
        Profile.objects.create(user=instance, first_name=instance.name)
        Resume.objects.create(user=instance)
