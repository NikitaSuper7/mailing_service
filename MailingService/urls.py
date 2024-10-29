from django.urls import path
from . import views
from MailingService.apps import MailingserviceConfig
from django.conf import settings
from django.conf.urls.static import static

app_name = MailingserviceConfig.name

urlpatterns = [
    path("clients/new", views.ClientCreateView.as_view(), name="client_form"),
    path("clients/", views.ClientListView.as_view(), name="client_list"),
    path("clients/<int:pk>", views.ClientDetailView.as_view(), name="client_detail"),
    path("clients/update/<int:pk>", views.ClientUpdateView.as_view(), name="client_update"),
    path("client/delete/<int:pk>", views.ClientDeleteView.as_view(), name="client_delete"),

    # path('success/', views.success, name='success')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)