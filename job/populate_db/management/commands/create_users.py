from django.core.management.base import BaseCommand
import random, string

from user_system.models import UserAccount, SeekerProfile

# Making array of real world names, cities, job_title, bio
names = [
    "Albana Doe",
    "Anil Sharma",
    "Fred",
    "Hari Tamang",
    "Hari Tiwari",
    "Ilias",
    "Jaydeep",
    "Jeong Kim",
    "John Doe",
    "Ram Adhikari",
    "Ramesh Chaudhary",
    "Ramika Shrestha",
    "Sita Karki",
    "Suraj",
    "Winston Rosenberg"
]
cities = [
    "Kathmandu",
    "Lalitpur",
    "Bhaktapur",
    "Pokhara",
    "Biratnagar",
    "Dharan",
    "Birgunj",
    "Janakpur",
    "Nepalgunj",
    "Butwal",
    "Dharan",
    "Birgunj",
    "Janakpur",
    "Nepalgunj",
    "Butwal",
]
job_titles = [
    "Software Engineer",
    "Full Stack Developer",
    "Data Scientist",
    "DevOps Engineer",
    "Product Manager",
    "UX Designer",
    "Machine Learning Engineer",
    "Mobile Developer",
    "Front-End Developer",
    "Back-End Developer",
    "UX Designer",
    "Machine Learning Engineer",
    "Mobile Developer",
    "Front-End Developer",
    "Back-End Developer",
]
bios = [
    "Experienced in developing, testing and deploying software applications. Proficient in multiple programming languages.",
    "Expert in building web applications using various technologies and frameworks. Keen eye for design and user experience.",
    "Skilled in using statistical models and algorithms to extract insights from data. Proficient in programming and data visualization.",
    "Well-versed in automating and optimizing software deployment processes. Strong understanding of cloud computing and infrastructure.",
    "Skilled in defining product strategies, conducting market research, and leading cross-functional teams to bring products to market.",
    "Experienced in designing user interfaces, conducting user research and testing, and creating wireframes and prototypes.",
    "Skilled in training and deploying machine learning models, and proficient in programming languages like Python and R.",
    "Expert in developing native mobile applications for iOS and Android platforms. Proficient in Swift and Java programming languages.",
    "Skilled in building responsive and dynamic user interfaces, and proficient in front-end development frameworks like React and Angular.",
    "Expert in building scalable and efficient back-end systems, and proficient in server-side programming languages like Python and Node.js.",
    "Experienced in designing user interfaces, conducting user research and testing, and creating wireframes and prototypes.",
    "Skilled in training and deploying machine learning models, and proficient in programming languages like Python and R.",
    "Expert in developing native mobile applications for iOS and Android platforms. Proficient in Swift and Java programming languages.",
    "Skilled in building responsive and dynamic user interfaces, and proficient in front-end development frameworks like React and Angular.",
    "Expert in building scalable and efficient back-end systems, and proficient in server-side programming languages like Python and Node.js.",
]
skills = ["C", "Python", "JavaScript", "SQL", "React", "Node.js", "Django", "Angular", "JS", "Java", "C++", "Go"]


def update_user_profile(user, i):
    profile, created = SeekerProfile.objects.get_or_create(user=user)
    profile.github = "https://github.com/torvalds"
    profile.linkedin = "https://www.linkedin.com/in/linustorvalds"
    profile.website = "https://linuxtorvalds.com/"
    profile.country = "Nepal"

    profile.job_title = job_titles[i]
    profile.bio = bios[i]
    profile.city = cities[i]
    profile.phone_number = "984" + "".join([str(random.randint(0, 9)) for _ in range(7)])

    selected_skills = random.sample(skills, 3)
    profile.skills = ", ".join(selected_skills)

    profile.save()


class Command(BaseCommand):
    help = "Create 10 instances of UserAccount and SeekerProfile"

    def handle(self, *args, **options):
        for i in range(15):
            email = f"user{i}@gmail.com"
            password = "testing321"

            # Create User
            user = UserAccount.objects.create_user(
                email=email,
                password=password,
                name=names[i],
                is_employer=False,
            )

            self.stdout.write('Account created for "%s"' % user.name)

            # Create Profile for above user
            update_user_profile(user, i)

            self.stdout.write('Profile updated for "%s"' % user.name)
