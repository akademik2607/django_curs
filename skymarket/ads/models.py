from django.conf import settings
from django.db import models


NULLABLE = {"null": True, "blank":True}


class Ad(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=100, default='')
    price = models.IntegerField(verbose_name="Цена", default=0)
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    image = models.ImageField(verbose_name="Изображение", default='')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now=True)

    class Meta:
        ordering = ['created_at']


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст", default='')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, **NULLABLE)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now=True)

