import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create default superuser if it does not exist"

    def handle(self, *args, **options):
        if os.getenv("CREATE_SUPERUSER") != "True":
            self.stdout.write("CREATE_SUPERUSER not enabled")
            return

        User = get_user_model()

        username = os.getenv("SUPERUSER_USERNAME", "choo")
        password = os.getenv("SUPERUSER_PASSWORD", "12345678")

        if User.objects.filter(username=username).exists():
            self.stdout.write("Superuser already exists")
            return

        User.objects.create_superuser(
            username=username,
            email="",
            password=password
        )

        self.stdout.write(self.style.SUCCESS("Superuser created"))