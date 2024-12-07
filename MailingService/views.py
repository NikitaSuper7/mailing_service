from django.shortcuts import render
from django.http import HttpResponse
from MailingService.models import Client, Mailing, Massage, Attemts
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from .forms import MailingForm
from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import smtplib
from users.models import CustomUser


# Create your views here.

# Контроллеры клиента

class ClientListView(LoginRequiredMixin, ListView):
    """List of client"""
    model = Client
    template_name = 'MailingService/client_list.html'
    context_object_name = 'clients'


class ClientCreateView(LoginRequiredMixin, CreateView):
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


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Client detail view"""
    model = Client
    template_name = 'MailingService/client_detail.html'
    context_object_name = 'client'


class ClientUpdateView(LoginRequiredMixin, UpdateView):
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


class ClientDeleteView(LoginRequiredMixin, DeleteView):
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

class MessageListView(LoginRequiredMixin, ListView):
    """Massage list view"""
    model = Massage
    template_name = 'MailingService/messages_list.html'
    context_object_name = 'messages'


class MessageCreateView(LoginRequiredMixin, CreateView):
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


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Massage detail view"""
    model = Massage
    template_name = 'MailingService/message_detail.html'
    context_object_name = 'message'


class MessageUpdateView(LoginRequiredMixin, UpdateView):
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


class MessageDeleteView(LoginRequiredMixin, DeleteView):
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
class MailingListView(LoginRequiredMixin, ListView):
    """Mailing list view"""
    model = Mailing
    template_name = 'MailingService/mailings_list.html'
    context_object_name = 'mailings'


class MainListView(LoginRequiredMixin, ListView):
    """Mailing list view"""
    model = Mailing
    template_name = 'MailingService/main_page.html'
    context_object_name = 'mailings'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings = self.model.objects.filter(owner=self.request.user)
        mailings_ids = [mailing.id for mailing in mailings]
        context['uniq_clients'] = Client.objects.filter(mailing__id__in=mailings_ids).distinct().count()
        context['mailings_total'] = self.model.objects.filter(owner=self.request.user).count()
        context['mailings_active'] = self.model.objects.filter(owner=self.request.user, message_states="Launched").count()
        context['mailings_completed'] = self.model.objects.filter(owner=self.request.user,
                                                               message_states="Compleated").count()
        # print(clients)
        return context

class ReportListView(LoginRequiredMixin, ListView):
    """Mailing list view"""
    model = Mailing
    template_name = 'MailingService/reports.html'
    context_object_name = 'mailings'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings = self.model.objects.filter(owner=self.request.user)
        mailings_ids = [mailing.id for mailing in mailings]
        context['total_attempts'] = Attemts.objects.filter(mailing__id__in=mailings_ids).count()
        context['success_attempts'] = Attemts.objects.filter(mailing__id__in=mailings_ids, state="Успешно").count()
        context['failed_attempts'] = Attemts.objects.filter(mailing__id__in=mailings_ids, state="Ошибка").count()

        return context




class MailingCreateView(LoginRequiredMixin, CreateView):
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
        recipient_list = [client.email for client in mailing.client.all()]
        # print(f"Отправляем письма на {recipient_list}")
        try:
            if mailing.message_states == mailing.LAUNCH_STATEMENT:
                server_response = send_mail(
                    subject=mailing.massage.topic,
                    message=mailing.massage.body,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
                attemt = Attemts.objects.create(mailing=mailing, server_response=server_response)
                if server_response:
                    attemt.state = "Успешно"
                    mailing.message_states = mailing.COMPLETE_STATEMENT
                    #     mailing.sent_at = datetime.now().date()
                attemt.save()

        except smtplib.SMTPException as exception:
            Attemts.objects.create(mailing=mailing, server_response=exception, state="Ошибка")
            mailing.message_states = mailing.COMPLETE_STATEMENT

        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Mailing detail view"""
    model = Mailing
    template_name = 'MailingService/mailing_detail.html'
    context_object_name = 'mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = self.object.client.count()
        return context


class MailingUpdateView(LoginRequiredMixin, UpdateView):
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
        try:
            if mailing.message_states == mailing.LAUNCH_STATEMENT:
                server_response = send_mail(
                    subject=mailing.massage.topic,
                    message=mailing.massage.body,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
                attemt = Attemts.objects.create(mailing=mailing, server_response=server_response)
                if server_response:
                    attemt.state = "Успешно"
                    mailing.message_states = mailing.COMPLETE_STATEMENT
                    #     mailing.sent_at = datetime.now().date()
                attemt.save()

        except smtplib.SMTPException as exception:
            Attemts.objects.create(mailing=mailing, server_response=exception, state="Ошибка")
            mailing.message_states = mailing.COMPLETE_STATEMENT

        # if mailing.message_states == mailing.LAUNCH_STATEMENT:
        #     send_mail(
        #         subject=subject,
        #         message=message,
        #         from_email=from_email,
        #         recipient_list=recipient_list
        #     )
        #     mailing.message_states = mailing.COMPLETE_STATEMENT
        #     mailing.sent_at = datetime.now().date()

        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
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


