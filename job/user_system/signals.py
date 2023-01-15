from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserAccount, Profile
from resume.models import Resume

@receiver(post_save, sender=UserAccount)
def create_profile_resume(sender, instance, created, **kwargs):
    """
    Signal to create profile and resume when user is created
    """
    if created:
        Profile.objects.create(user=instance, first_name=instance.name)
        Resume.objects.create(user=instance)
        print('created profile and resume')

@receiver(post_save, sender=UserAccount)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.resume.save()