from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from users.models import CustomUser

# Для генерации токена:
import secrets

# Импорт емейла:
from config.settings import EMAIL_HOST_USER

# Create your views here.

class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('MailingService:mailings_list')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        subject = 'Добро пожаловать в наш сервис рассылок!'
        message = f"""Спасибо, что зарегистрировались в нашем сервисе рассылок!
        Для подтверждения почты перейдите по ссылке {url}"""

        from_email = EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list
        )
        return super().form_valid(form)

def email_verification(request, token):
    """Верификация email"""
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))

class UserDetailView(LoginRequiredMixin, DetailView):
    """Client detail view"""
    model = CustomUser
    template_name = 'users/user_detail.html'
    context_object_name = 'current_user'
class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Client update view"""
    model = CustomUser
    fields = ['email', 'username', 'phone_number', 'avatar']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('MailingService:main_page')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object:
            self.object.save()
            return self.object
        raise PermissionDenied

