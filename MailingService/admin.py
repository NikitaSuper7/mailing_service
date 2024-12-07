from django.contrib import admin
from .models import Client, Mailing, Massage, Attemts
# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "comment")
    list_filter = ("full_name", "email",)
    search_fields = ("full_name", "email",)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "message_states", "created_at", "sent_at", "end_send_at")
    list_filter = ("name", "message_states", "created_at", "sent_at", "end_send_at")
    search_fields = ("name", "massage")

@admin.register(Massage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "body", )
    list_filter = ("topic",)
    search_fields = ("topic", "body",)

@admin.register(Attemts)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "datetime", "state", "server_response", "mailing",)
    list_filter = ("datetime", "state", "mailing",)
    search_fields = ("datetime", "state", "mailing", "server_response",)
