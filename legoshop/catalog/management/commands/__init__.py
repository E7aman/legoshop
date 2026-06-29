from django.core.management.base import BaseCommand
from legoshop.accounts.models import User

class Command(BaseCommand):
    help = 'Автоматическое создание суперпользователя'

    def handle(self, *args, **options):
        username = 'admin1'
        password = 'qwerty77!'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email='', password=password)
            self.stdout.write(self.style.SUCCESS(f'Суперпользователь {username} создан!'))
        else:
            self.stdout.write(self.style.WARNING(f'Суперпользователь {username} уже есть.'))