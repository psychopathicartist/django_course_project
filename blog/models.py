from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    """
    Модель блога для сайта рассылок
    """

    heading = models.CharField(max_length=200, verbose_name='заголовок')
    content = models.CharField(max_length=500, verbose_name='содержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='превью', **NULLABLE)
    created_at = models.DateField(auto_now_add=True, verbose_name='дата публикации')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.heading}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'

