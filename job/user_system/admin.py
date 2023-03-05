from django.contrib import admin
from .models import SeekerProfile, EmployerProfile, UserAccount

admin.site.register(UserAccount)
admin.site.register(SeekerProfile)
admin.site.register(EmployerProfile)