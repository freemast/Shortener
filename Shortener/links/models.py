from django.db import models
from django.contrib.auth import get_user_model
from random import choice
import string

User = get_user_model()

def gen_short():
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(choice(chars) for _ in range(6))

class Tags(models.Model):
    title = models.CharField("Заголовок тега", max_length=100)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.title

class Links(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    title = models.CharField("Заголовок ссылки", max_length=100)
    description = models.TextField("Описание ссылки", max_length=500)
    original_url = models.URLField("Оригинальная ссылка")
    short_url = models.CharField("Короткая ссылка", max_length=6, unique=True, default=gen_short)
    tags = models.ManyToManyField(Tags, verbose_name="Теги")
    created = models.DateTimeField("Дата создания ссылки", auto_now_add=True)
    jump = models.IntegerField("Переходы", default=0)

    class Meta:
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"

    def __str__(self):
        return self.title