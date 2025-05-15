# pushapp/models.py

from django.db import models
from django.conf import settings


class PushSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    endpoint = models.TextField()
    auth = models.CharField(max_length=256)
    p256dh = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'endpoint')

    def __str__(self):
        return f"{self.user.username} — {self.endpoint[:50]}"
  


