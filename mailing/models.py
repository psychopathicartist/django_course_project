from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """
    Модель клиента сервиса (тот, кому будет отправляться рассылка)
    """
    email = models.EmailField(verbose_name='почта')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    comment = models.CharField(max_length=300, verbose_name='комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.email} - {self.full_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """
    Модель сообщения рассылки
    """
    subject = models.CharField(max_length=150, verbose_name='тема')
    content = models.CharField(max_length=500, verbose_name='содержание')

    def __str__(self):
        return f'{self.subject}: {self.content}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    """
    Модель рассылки, имеет связь с моделями Клиент и Сообщение
    """

    EVERY_TWO_HOURS = 'Каждые 2 часа'
    DAILY = 'Ежедневно'
    WEEKLY = 'Еженедельно'
    MONTHLY = 'Ежемесячно'

    PERIODS = [
        (EVERY_TWO_HOURS, 'Каждые 2 часа'),
        (DAILY, 'Ежедневно'),
        (WEEKLY, 'Еженедельно'),
        (MONTHLY, 'Ежемесячно'),
    ]

    STATUS_CREATED = 'Создана'
    STATUS_STARTED = 'Запущена'
    STATUS_COMPLETED = 'Завершена'

    STATUSES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_COMPLETED, 'Завершена'),
    ]

    start_time = models.TimeField(verbose_name='время начала рассылки')
    end_time = models.TimeField(verbose_name='время окончания рассылки')
    period = models.CharField(max_length=25, choices=PERIODS, verbose_name='период рассылки')
    status = models.CharField(default='created', max_length=25, choices=STATUSES, verbose_name='статус рассылки')
    clients = models.ManyToManyField(Client, verbose_name='клиенты')
    message = models.OneToOneField(Message, on_delete=models.CASCADE, verbose_name='сообщение')

    def __str__(self):
        return f'{self.period} ({self.message})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Log(models.Model):
    """
    Модель попытки рассылки
    """
    STATUSES = {
        'failed': 'Ошибка',
        'finished': 'Успешно завершена',
    }

    last_date_and_time = models.DateTimeField(auto_now_add=timezone.now, verbose_name='дата и время последней рассылки')
    status = models.CharField(default='created', max_length=15, choices=STATUSES, verbose_name='статус попытки рассылки')
    server_answer = models.CharField(max_length=300, verbose_name='ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
