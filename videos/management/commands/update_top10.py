from django.core.management.base import BaseCommand
from videos.models import Video
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Обновляет список топ-10 видео каждые 10 дней"

    def handle(self, *args, **kwargs):
        ten_days_ago = timezone.now() - timedelta(days=10)
        top_videos = Video.objects.filter(time_create__gte=ten_days_ago).order_by('-rating')[:10]

        # Например, можно сохранить список в кэш
        from django.core.cache import cache
        cache.set('top10_videos', top_videos, timeout=86400 * 10)  # Кэшируем на 10 дней

        self.stdout.write(self.style.SUCCESS('Топ-10 видео обновлен'))
        