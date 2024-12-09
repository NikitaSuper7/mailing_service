from django.urls import path
from .views import RegisterView, email_verification, UserUpdateView, UserDetailView, UserListView, ManagerUpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView

from users.apps import UsersConfig
from django.urls import reverse_lazy


app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(success_url=reverse_lazy('users:login')), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html',
                                     success_url=reverse_lazy('catalog:main_page')), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    # путь для верификации почты:
    path("email-confirm/<str:token>/", email_verification, name='email-confirm'),
    # Шаблоны для сброса пароля:
    path('password-reset/', PasswordResetView.as_view(template_name='users/reset_password.html',
                                                      email_template_name='users/password_reset_email.html',
                                                      success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url=reverse_lazy('users:password_reset_complete'),),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    # Для редактирования профиля:
    path("users/<int:pk>", UserDetailView.as_view(), name="user_detail"),
    path("users/update/<int:pk>", UserUpdateView.as_view(), name="user_update"),
    # Для модераторов:
    path('users/', UserListView.as_view(), name="users_list"),
    path("users/manager_update/<int:pk>", ManagerUpdateView.as_view(), name="manager_update"),

]
