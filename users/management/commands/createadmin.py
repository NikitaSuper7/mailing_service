from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            email='testadmin@mail.ru',
            first_name='Admin',
            lasst_name='Admin',
        )

        user.set_password('Nikita130296')

        user.is_stuff = True
        user.is_superuser = True

        self.stdout.write(self.style.SUCCES(f"Successfully created admin with email - {user.email}"))

        user.save()