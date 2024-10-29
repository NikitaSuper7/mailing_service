from django.db import models


# Create your models here.

class Client(models.Model):
    """Модель клиента сообщения."""
    full_name = models.CharField(max_length=200, verbose_name='ФИО клиента', help_text='Введите ФИО клиента')
    email = models.EmailField(verbose_name='Email клиента', help_text='Введите email клиента', unique=True)
    comment = models.TextField(
        verbose_name='Комментарий клиента',
        help_text='Введите комментарий клиента',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.full_name}, email -{self.email}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Massage(models.Model):
    """Модель сообщения"""
    topic = models.CharField(max_length=200, verbose_name='Тема сообщения', help_text='Введите тему сообщения')
    body = models.TextField(
        verbose_name='Текст сообщения',
        help_text='Введите текст сообщения',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.topic}, {self.body}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    """Модель рассылки"""
    CREATE_STATEMENT = 'Created'
    LAUNCH_STATEMENT = 'Launched'
    COMPLETE_STATEMENT = 'Compleated'

    STATE_CHOICES = [
        (CREATE_STATEMENT, 'Создана'),
        (LAUNCH_STATEMENT, 'Запущена'),
        (COMPLETE_STATEMENT, 'Завершена'),
    ]

    client = models.ManyToManyField(Client, verbose_name='Клиент')
    massage = models.ForeignKey(Massage, on_delete=models.CASCADE, verbose_name='Сообщение')
    message_states = models.CharField(max_length=10, choices=STATE_CHOICES, default=CREATE_STATEMENT)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    sent_at = models.DateTimeField(null=True, verbose_name='Дата и время начала отправки')
    end_send_at = models.DateTimeField(null=True, verbose_name='Дата и время окончания отправки')

    def __str__(self):
        return f'{self.massage} {self.created_at}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['created_at', 'sent_at']
