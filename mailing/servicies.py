from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Log


def send_mailing(mailing):
    """
    Функция отправляет письма рассылки и создает ее лог в
    зависимости от ответа сервера
    """
    try:
        send_mail(
            subject=mailing.message.subject,
            message=mailing.message.content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.clients.all()],
            fail_silently=False
        )

        Log.objects.create(
            status='Успешно завершена',
            mailing=mailing,
            server_answer='Рассылка отправлена'
        )

    except SMTPException as error:
        Log.objects.create(
            status='Ошибка',
            mailing=mailing,
            server_answer=error
        )
