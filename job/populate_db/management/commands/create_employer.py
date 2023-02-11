from django.core.management.base import BaseCommand

from user_system.models import UserAccount, EmployerProfile

company_names = [
    "Microsoft",
    "Netflix",
    "NepBay",
    "YetiHub",
    "Techminds Group",
    "Mount Technologies",
    "KU Tech",
    "Everest Innovation",
    "Sastodeal",
    "ICC",
]

company_locations = [
    "New York",
    "California",
    "Pokhara",
    "Kathmandu",
    "Kathmandu",
    "Lalitpur",
    "Lalitpur",
    "Bhaktapur",
    "Pokhara",
    "Dharan",
]
company_description = "Multinational company that provides IT and software solutions for businesses, helping to drive digital growth in the region. The company's focus is to create software that improves efficiency, streamlines processes and drives growth for their clients. Their team consists of highly skilled professionals including software developers, designers, and project managers who work together to bring innovative ideas to life. The company's focus is to create software that improves efficiency, streamlines processes and drives growth for their clients. Their team consists of highly skilled professionals including software developers, designers, and project managers who work together to bring innovative ideas to life."


def update_employer_profile(user, i):
    profile, created = EmployerProfile.objects.get_or_create(user=user)
    profile.linkedin = "https://www.linkedin.com/company/microsoft/"
    profile.website = "https://www.microsoft.com/"
    profile.contact_email = "info@microsoft.com"
    profile.country = "Nepal"


    profile.company_name = company_names[i]
    profile.company_location = company_locations[i]
    profile.company_description = company_description

    profile.save()


class Command(BaseCommand):
    help = "Create 10 instances of UserAccount and EmployerProfile"

    def handle(self, *args, **options):
        for i in range(10):
            email = f"company{i}@gmail.com"
            password = "testing321"

            # Create User
            user = UserAccount.objects.create_user(
                email=email,
                password=password,
                name=company_names[i],
                is_employer=True,
            )

            # Create Profile for above user
            update_employer_profile(user, i)

            self.stdout.write('Account and Profile created for "%s"' % user.name)
