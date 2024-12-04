from django.urls import path
from .views import RegisterView, email_verification
from django.contrib.auth.views import LoginView, LogoutView
from users.apps import UsersConfig
from django.urls import reverse_lazy


app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(success_url=reverse_lazy('users:login')), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html',
                                     success_url=reverse_lazy('catalog:main_page')), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    # путь для верификации почты:
    path("email-confirm/<str:token>/", email_verification, name='email-confirm')
]