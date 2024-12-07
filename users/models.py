from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to="media/photos",
                               blank=True,
                               null=True,
                               verbose_name="Изображение",
                               help_text="Загрузите изображение продукта", )
    token = models.CharField(max_length=100, verbose_name="token", blank=True, null=True)

    # Поля для авторизации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.email
