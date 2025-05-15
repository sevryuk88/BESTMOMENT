from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    updated_at = models.DateTimeField(auto_now=True)  # Добавляем дату обновления
    subscribers = models.ManyToManyField('self', symmetrical=False, related_name='subscriptions', blank=True)
    
    
    
