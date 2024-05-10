from django.contrib import admin

from mailing.models import Mailing, Message, Client, Log


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'period', 'status', 'message',)


@admin.register(Message)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'content',)


@admin.register(Client)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'comment',)


@admin.register(Log)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_date_and_time', 'status', 'server_answer', 'mailing',)
