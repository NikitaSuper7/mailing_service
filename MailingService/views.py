from django.shortcuts import render
from django.http import HttpResponse
from MailingService.models import Client, Mailing, Massage
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


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


class ClientDeleteView(DeleteView):
    """Client delete view"""
    model = Client
    template_name = 'MailingService/client_confirm_delete.html'
    # context_object_name = 'client'


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


class MessageDeleteView(DeleteView):
    """Massage delete view"""
    model = Massage
    template_name = 'MailingService/message_confirm_delete.html'
    context_object_name = 'message'


# Контроллеры для рассылки
class MailingListView(ListView):
    """Mailing list view"""
    model = Mailing
    template_name = 'MailingService/mailings_list.html'
    context_object_name = 'mailings'

class MailingCreateView(CreateView):
    """Mailing create view"""
    model = Mailing
    fields = ['name', 'client', 'massage']
    template_name = 'MailingService/mailing_form.html'
    success_url = reverse_lazy("MailingService:mailings_list")

class MailingDetailView(DetailView):
    """Mailing detail view"""
    model = Mailing
    template_name = 'MailingService/mailing_detail.html'
    context_object_name = 'mailing'

class MailingUpdateView(UpdateView):
    """Mailing update view"""
    model = Mailing
    fields = fields = ['name', 'client', 'massage']
    template_name = 'MailingService/mailing_form.html'
    success_url = reverse_lazy("MailingService:mailings_list")

class MailingDeletView(DeleteView):
    """Mailing delete view"""
    model = Mailing
    template_name = "MailingService/mailing_confirm_delete.html"
    context_object_name = 'mailing'

