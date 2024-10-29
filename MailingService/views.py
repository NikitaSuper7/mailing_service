from django.shortcuts import render
from django.http import HttpResponse
from MailingService.models import Client, Mailing, Massage
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

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
    context_object_name = 'client'