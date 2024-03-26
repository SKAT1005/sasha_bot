from django.db import models

class Congratulations(models.Model):
    author = models.CharField(max_length=64, verbose_name='Автор ')
    text = models.TextField(verbose_name='Текст поздравления')
    photo = models.ImageField(upload_to='congratulations/', blank=True, null=True, verbose_name='Фотография к поздравлению')


class Memories(models.Model):
    text = models.TextField(verbose_name='Текст воспоминания')
    photo = models.ImageField('memory_photo/', blank=True, null=True)


