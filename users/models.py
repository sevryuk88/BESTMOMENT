from django.db import models
from django.contrib.auth.models import AbstractUser
from storages.backends.s3boto3 import S3Boto3Storage  # Добавим импорт

# Кастомное хранилище для фото (можно не указывать location, если не нужно)
class MediaStorage(S3Boto3Storage):
    location = 'users'  # Это добавит префикс 'users/' ко всем загружаемым изображениям

class User(AbstractUser):
    photo = models.ImageField(
        upload_to="%Y/%m/%d/",
        storage=MediaStorage(),  # Вот здесь мы явно указываем хранилище
        blank=True,
        null=True,
        verbose_name="Фотография"
    )
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    updated_at = models.DateTimeField(auto_now=True)
    subscribers = models.ManyToManyField('self', symmetrical=False, related_name='subscriptions', blank=True)
    
