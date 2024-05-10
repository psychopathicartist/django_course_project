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
    class Meta:
        model = Mailing
        exclude = ['status']


class ClientForm(StyleForMixin, forms.ModelForm):
    """
    Класс для отображения формы модели клиента
    """
    class Meta:
        model = Client
        fields = '__all__'


class MessageForm(StyleForMixin, forms.ModelForm):
    """
    Класс для отображения формы модели сообщения
    """
    class Meta:
        model = Message
        fields = '__all__'
