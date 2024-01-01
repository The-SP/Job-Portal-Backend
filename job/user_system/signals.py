from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserAccount, SeekerProfile, EmployerProfile
# from resume.models import Resume


@receiver(post_save, sender=UserAccount)
def create_profile_resume(sender, instance, created, **kwargs):
    """
    Signal to create profile and resume when Seeker user is created
    """
    if created:
        if instance.is_employer:
            EmployerProfile.objects.create(user=instance, company_name=instance.name)
        else:
            SeekerProfile.objects.create(user=instance, name=instance.name, email=instance.email)
            # Resume.objects.create(user=instance)
