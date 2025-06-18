from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='Admin@123456'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
            self.stdout.write('Username: admin')
            self.stdout.write('Password: Admin@123456')
        else:
            self.stdout.write('Superuser already exists!')