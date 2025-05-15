# videos/tasks.py
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
#from .models import Video, VideoView




@shared_task
def increment_view_count(video_id, user_id=None):
    """ Увеличивает счётчик просмотров видео асинхронно и создаёт запись VideoView """
    from videos.models import Video, VideoView, User

    try:
        video = Video.objects.get(id=video_id)
        user = User.objects.get(id=user_id) if user_id else None

        # Проверим, не существует ли уже просмотр
        obj, created = VideoView.objects.get_or_create(video=video, user=user)
        if created:
            # Только при новом просмотре увеличиваем рейтинг
            Video.objects.filter(id=video_id).update(rating=F('rating') + 1)

        return {'success': f'Просмотр засчитан для видео {video_id}, пользователь: {user_id}'}

    except Video.DoesNotExist:
        return {'error': 'Видео не найдено'}
    except User.DoesNotExist:
        return {'error': 'Пользователь не найден'}
        
"""
#  Фоновая задача Celery для подсчёта просмотров
@shared_task
def increment_view_count(video_id):
     Увеличивает счётчик просмотров видео асинхронно 
    from videos.models import Video, VideoView  # Импортируем внутри функции, чтобы избежать цикла
    
    try:
        Video.objects.filter(id=video_id).update(rating=F('rating') + 1)
        video = Video.objects.get(id=video_id)
        VideoView.objects.update_or_create(video=video, user=None, defaults={})
        
       # VideoView.objects.get_or_create(video=video, user=None)  # Если нет user — анонимный просмотр
    except Video.DoesNotExist:
        return {'error': 'Видео не найдено'}
    return {'success': f'Просмотр засчитан для видео {video_id}'}
"""


@shared_task
def update_top_videos():
    from videos.models import Video
    from django.core.cache import cache
    from django.utils import timezone
    from datetime import timedelta

    ten_days_ago = timezone.now() - timedelta(days=10)
    top_videos = list(Video.objects.filter(time_create__gte=ten_days_ago).order_by('-rating')[:10])

    # Сохраняем список ID (можно и сериализовать объекты, но проще ID)
    top_video_ids = [video.id for video in top_videos]
    cache.set('top_videos', top_video_ids, timeout=864000)

    return {'success': f'ТОП-10 видео обновлены. Кол-во: {len(top_videos)}'}
        
    

    
@shared_task
def update_video_rating(video_id):
    """Обновляет рейтинг видео"""
    from videos.models import Video  # Импортируем здесь

    try:
        video = Video.objects.get(id=video_id)
        video.rating = video.likes_count - video.dislikes_count
        video.save(update_fields=['rating'])
    except Video.DoesNotExist:
        return {'error': 'Видео не найдено'}
    return {'success': f'Рейтинг обновлён для видео {video_id}'}
    

#  Очистка устаревших данных (для оптимизации базы)
@shared_task
def clean_old_data():
    """ Удаляет старые видео, которым более 1 года """
    from videos.models import Video  # Импортируем здесь
    
    one_year_ago = timezone.now() - timedelta(days=365)
    deleted_count, _ = Video.objects.filter(time_create__lt=one_year_ago).delete()
    
    return {'success': f'Удалено старых видео: {deleted_count}'}
    