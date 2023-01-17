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
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    # avatar = models.ImageField(
    #     max_length=255, upload_to="profile_images/", null=True, blank=True
    # )
    bio = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name


class EmployerProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=100)
    company_description = models.TextField(null=True, blank=True)
    company_website = models.URLField(null=True, blank=True)
    company_location = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    contact_email = models.EmailField(
        max_length=100, unique=True, null=True, blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    # company_logo = models.ImageField(upload_to='employer_logos/', null=True, blank=True)
