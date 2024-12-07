import smtplib
from datetime import datetime
from django.core.mail import send_mail
from pytz import timezone
from config import settings
from MailingService.models import Attemts, Mailing
from django.core.management import BaseCommand
from config.settings import EMAIL_HOST_USER


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.attemts_mailing()

    def attemts_mailing(self):
        """Отправляем рассылку"""
        zone = timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)
        for mailing in Mailing.objects.filter(message_states="Launched"):
            if mailing.sent_at and mailing.end_send_at and mailing.sent_at < current_datetime < mailing.end_send_at:
                try:
                    mails = [client.email for client in mailing.client.all()]
                    server_response = send_mail(
                        subject=mailing.massage.topic,
                        message=mailing.massage.body,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=mails,
                        fail_silently=False,
                    )
                    attemt = Attemts.objects.create(mailing=mailing, server_response=server_response)
                    if server_response:
                        attemt.state = "Успешно"
                    attemt.save()

                except smtplib.SMTPException as exception:
                    Attemts.objects.create(mailing=mailing, server_response=exception, state="Ошибка")
