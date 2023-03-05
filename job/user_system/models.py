from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # To handle multiple user types (Seeker and Employer)
    is_employer = models.BooleanField(default=False)

    objects = UserAccountManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "is_employer"]

    def __str__(self):
        return self.email


class SeekerProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True, related_name='seeker_profile')
    # avatar = models.ImageField(
    #     max_length=255, upload_to="profile_images/", null=True, blank=True
    # )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    skills = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EmployerProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True, related_name='company')
    company_name = models.CharField(max_length=100)
    company_location = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    company_description = models.TextField(null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    contact_email = models.EmailField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # company_logo = models.ImageField(upload_to='employer_logos/', null=True, blank=True)

    def __str__(self):
        return self.company_name