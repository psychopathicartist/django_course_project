import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore

from mailing.models import Mailing, Log
from mailing.servicies import send_mailing

logger = logging.getLogger(__name__)
scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)


def change_status():
    """
    Функция для периодического вызова, которая меняет статус рассылки в зависимости
    от текущего времени и времени начала и окончания рассылки
    """
    for mailing in Mailing.objects.all():
        if timezone.now().time() < mailing.start_time:
            mailing.status = 'Создана'
        elif mailing.start_time <= timezone.now().time() <= mailing.end_time:
            mailing.status = 'Запущена'
        else:
            mailing.status = 'Завершена'
            if Log.objects.filter(mailing=mailing).exists():
                scheduler.remove_job(mailing.pk)
        mailing.save()


class Command(BaseCommand):
    """
    Кастомная команда, которая запускается из консоли и запускает планировщик
    для выполнения периодических задач
    """

    help = "Runs APScheduler."

    def handle(self, *args, **options):

        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            change_status,
            trigger=CronTrigger(second='*/30'),
            id=f'change_status',
            max_instances=1,
            replace_existing=True,
        )

        # Для рассылки в статусе запущена происходит выполнение периодической задачи
        mailings_running = Mailing.objects.filter(status='Запущена')
        for mailing in mailings_running:
            logs = Log.objects.filter(mailing=mailing)
            if not logs.exists():
                if mailing.period == 'Каждые 2 часа':
                    scheduler.add_job(
                        send_mailing,
                        trigger='interval',
                        minutes=2,  # Заменено на каждые 2 минуты для удобства проверки
                        id=f'{mailing.pk}',
                        args=[mailing],
                        max_instances=1,
                        replace_existing=True,
                    )
                else:
                    if mailing.period == 'Ежедневно':
                        cron_period = CronTrigger(day='*/1')
                    elif mailing.period == 'Еженедельно':
                        cron_period = CronTrigger(week='*/1')
                    else:
                        cron_period = CronTrigger(month='*/1')
                    scheduler.add_job(
                        send_mailing,
                        trigger=cron_period,
                        id=f'{mailing.pk}',
                        args=[mailing],
                        max_instances=1,
                        replace_existing=True,
                    )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
