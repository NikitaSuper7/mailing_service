from django.urls import path
from . import views
from MailingService.apps import MailingserviceConfig
from django.conf import settings
from django.conf.urls.static import static

app_name = MailingserviceConfig.name

urlpatterns = [
    # Clients URLs
    path("clients/new", views.ClientCreateView.as_view(), name="client_form"),
    path("clients/", views.ClientListView.as_view(), name="client_list"),
    path("clients/<int:pk>", views.ClientDetailView.as_view(), name="client_detail"),
    path("clients/update/<int:pk>", views.ClientUpdateView.as_view(), name="client_update"),
    path("client/delete/<int:pk>", views.ClientDeleteView.as_view(), name="client_delete"),

    # Message URLs
    path("messages/", views.MessageListView.as_view(), name="messages_list"),
    path("messages/new", views.MessageCreateView.as_view(), name="message_form"),
    path("messages/<int:pk>", views.MessageDetailView.as_view(), name='message_detail'),
    path("messages/update/<int:pk>", views.MessageUpdateView.as_view(), name='message_update'),
    path("message/delete/<int:pk>", views.MessageDeleteView.as_view(), name="message_delete"),

    # Mailing URLs
    path("mailings/new", views.MailingCreateView.as_view(), name="mailing_form"),
    path("mailings/", views.MailingListView.as_view(), name="mailings_list"),
    path("mailings/<int:pk>", views.MailingDetailView.as_view(), name="mailing_detail"),
    path("mailings/update/<int:pk>", views.MailingUpdateView.as_view(), name='mailing_update'),
    path("mailing/delete/<int:pk>", views.MailingDeleteView.as_view(), name="mailing_delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)