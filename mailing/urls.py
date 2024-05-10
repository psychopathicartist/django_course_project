from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MailingListView, MailingCreateView, MailingDeleteView, MailingDetailView, MailingUpdateView, \
    ClientListView, ClientDeleteView, ClientUpdateView, ClientDetailView, ClientCreateView, MessageListView, \
    MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView, MainView, LogListView

app_name = MailingConfig.name

urlpatterns = [
    path('', MainView.as_view(), name='main'),

    path('list/', MailingListView.as_view(), name='list'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('mailing/<int:pk>', MailingDetailView.as_view(), name='view'),
    path('edit/<int:pk>', MailingUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', MailingDeleteView.as_view(), name='delete'),

    path('client-list/', ClientListView.as_view(), name='client_list'),
    path('client-create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>', ClientDetailView.as_view(), name='client_view'),
    path('client-edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('client-delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),

    path('message-list/', MessageListView.as_view(), name='message_list'),
    path('message-create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message_view'),
    path('message-edit/<int:pk>', MessageUpdateView.as_view(), name='message_edit'),
    path('message-delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

    path('log/', LogListView.as_view(), name='log_list'),
]
