from django.shortcuts import render
from django.http import HttpResponse
from MailingService.models import Client, Mailing, Massage
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from .forms import MailingForm
from datetime import datetime
from django.core.exceptions import PermissionDenied


# Create your views here.

# Контроллеры клиента

class ClientListView(ListView):
    """List of client"""
    model = Client
    template_name = 'MailingService/client_list.html'
    context_object_name = 'clients'


class ClientCreateView(CreateView):
    """Create a new client"""
    model = Client
    fields = ['full_name', 'email', 'comment']
    template_name = 'MailingService/client_form.html'
    success_url = reverse_lazy('MailingService:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientDetailView(DetailView):
    """Client detail view"""
    model = Client
    template_name = 'MailingService/client_detail.html'
    context_object_name = 'client'


class ClientUpdateView(UpdateView):
    """Client update view"""
    model = Client
    fields = ['full_name', 'email', 'comment']
    template_name = 'MailingService/client_form.html'
    success_url = reverse_lazy('MailingService:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionDenied


class ClientDeleteView(DeleteView):
    """Client delete view"""
    model = Client
    template_name = 'MailingService/client_confirm_delete.html'
    success_url = reverse_lazy('MailingService:client_list')
    # context_object_name = 'client'
    def get_object(self, queryset=None):
        """
        Переопределяем метод get_object для проверки доступа.
        """
        client = super().get_object(queryset)
        user = self.request.user

        # Проверяем, является ли пользователь владельцем или имеет нужное разрешение
        if client.owner == user:
            return client

        # Если пользователь не авторизован для удаления
        raise PermissionDenied("У вас нет прав на удаление этого клиента.")


# Контроллеры сообщения:

class MessageListView(ListView):
    """Massage list view"""
    model = Massage
    template_name = 'MailingService/messages_list.html'
    context_object_name = 'messages'


class MessageCreateView(CreateView):
    """Massage create view"""
    model = Massage
    fields = ['topic', 'body']
    template_name = 'MailingService/message_form.html'
    success_url = reverse_lazy('MailingService:messages_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageDetailView(DetailView):
    """Massage detail view"""
    model = Massage
    template_name = 'MailingService/message_detail.html'
    context_object_name = 'message'


class MessageUpdateView(UpdateView):
    """Massage update view"""
    model = Massage
    fields = ['topic', 'body']
    template_name = 'MailingService/message_form.html'
    success_url = reverse_lazy('MailingService:messages_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionDenied


class MessageDeleteView(DeleteView):
    """Massage delete view"""
    model = Massage
    template_name = 'MailingService/message_confirm_delete.html'
    context_object_name = 'message'
    success_url = reverse_lazy('MailingService:messages_list')

    def get_object(self, queryset=None):
        """
        Переопределяем метод get_object для проверки доступа.
        """
        message = super().get_object(queryset)
        user = self.request.user
        if message.owner == user:
            return message
        raise PermissionDenied("У вас нет прав на удаление этого сообщения.")


# Контроллеры для рассылки
class MailingListView(ListView):
    """Mailing list view"""
    model = Mailing
    template_name = 'MailingService/mailings_list.html'
    context_object_name = 'mailings'


class MailingCreateView(CreateView):
    """Mailing create view"""
    model = Mailing
    form_class = MailingForm
    # fields = ['name', 'client', 'massage']
    template_name = 'MailingService/mailing_form.html'
    success_url = reverse_lazy("MailingService:mailings_list")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        host = self.request.get_host()
        # url = f"http://{host}/users/mailing-email/"
        subject = mailing.massage.topic
        message = f"""{mailing.massage.body}"""

        from_email = EMAIL_HOST_USER
        # for client in mailing.client.all():
        #     print(f"Клиенты {client.email}")
        recipient_list = [client.email for client in mailing.client.all()]
        print(f"Отправляем письма на {recipient_list}")
        if mailing.message_states == mailing.LAUNCH_STATEMENT:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list
            )
            mailing.message_states = mailing.COMPLETE_STATEMENT
            mailing.sent_at = datetime.now().date()
        return super().form_valid(form)


class MailingDetailView(DetailView):
    """Mailing detail view"""
    model = Mailing
    template_name = 'MailingService/mailing_detail.html'
    context_object_name = 'mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = self.object.client.count()
        return context


class MailingUpdateView(UpdateView):
    """Mailing update view"""
    model = Mailing
    form_class = MailingForm
    # fields = fields = ['name', 'client', 'massage']
    template_name = 'MailingService/mailing_form.html'
    success_url = reverse_lazy("MailingService:mailings_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionDenied

    def form_valid(self, form):
        mailing = form.save()
        mailing.save()
        host = self.request.get_host()
        # url = f"http://{host}/users/mailing-email/"
        subject = mailing.massage.topic
        message = f"""{mailing.massage.body}"""

        from_email = EMAIL_HOST_USER
        # for client in mailing.client.all():
        #     print(f"Клиенты {client.email}")
        recipient_list = [client.email for client in mailing.client.all()]
        print(f"Отправляем письма на {recipient_list}")
        if mailing.message_states == mailing.LAUNCH_STATEMENT:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list
            )
            mailing.message_states = mailing.COMPLETE_STATEMENT
            mailing.sent_at = datetime.now().date()
        return super().form_valid(form)


class MailingDeleteView(DeleteView):
    """Mailing delete view"""
    model = Mailing
    template_name = "MailingService/mailing_confirm_delete.html"
    context_object_name = 'mailing'
    success_url = reverse_lazy("MailingService:mailings_list")

    def get_object(self, queryset=None):
        mailing = super().get_object(queryset)
        user = self.request.user

        if mailing.owner == user:
            return mailing
        raise PermissionDenied("У вас нет прав на удаление этой рассылки.")
