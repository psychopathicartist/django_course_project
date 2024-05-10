from django import forms

from mailing.models import Mailing, Message, Client


class StyleForMixin:
    """
    Миксин класс для отображения форм
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleForMixin, forms.ModelForm):
    """
    Класс для отображения формы модели рассылки
    """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(author=user)
        self.fields['message'].queryset = Message.objects.filter(author=user)

    class Meta:
        model = Mailing
        exclude = ['author', 'status']


class ClientForm(StyleForMixin, forms.ModelForm):
    """
    Класс для отображения формы модели клиента
    """
    class Meta:
        model = Client
        exclude = ['author']


class MessageForm(StyleForMixin, forms.ModelForm):
    """
    Класс для отображения формы модели сообщения
    """
    class Meta:
        model = Message
        exclude = ['author']


class PermMailingForm(StyleForMixin, forms.ModelForm):
    """
    Класс для отображения формы модели рассылки
    для редактирования менеджером
    """
    class Meta:
        model = Mailing
        fields = ['status']
