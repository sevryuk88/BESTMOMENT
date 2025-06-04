# videos/tasks.py
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
#from .models import Video, VideoView




@shared_task
def increment_view_count(video_id):
    from videos.models import VideoView  # Только нужное
   

    try:
        # Минимизируем использование ORM
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("UPDATE videos_video SET rating = rating + 1 WHERE id = %s", [video_id])
        
        # Только одна простая запись
        VideoView.objects.get_or_create(video_id=video_id, user=None)
        
    except Exception as e:
        return {'error': str(e)}
    
    return {'success': f'Просмотр засчитан для видео {video_id}'}
    


"""
@shared_task
def increment_view_count(video_id, user_id=None):
    from videos.models import Video, VideoView
    from django.contrib.auth.models import User

    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return {"error": "Видео не найдено"}

    user = None
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass

    # Проверка: был ли просмотр
    obj, created = VideoView.objects.get_or_create(video=video, user=user)

    if created:
        # обновляем рейтинг вручную (т.к. view_count — property)
        video.rating += 1
        video.save()

    return {
        "message": "Просмотр засчитан",
        "view_count": video.video_views.count()
    }
    



@shared_task
def increment_view_count(video_id, user_id=None):
    from videos.models import Video, VideoView, User

    try:
        video = Video.objects.get(id=video_id)
        user = User.objects.get(id=user_id) if user_id else None

        # Проверим, не существует ли уже просмотр
        obj, created = VideoView.objects.get_or_create(video=video, user=user)
        if created:
            # Только при новом просмотре увеличиваем рейтинг
            video.rating += 1
            video.save()

        return {
            'message': 'Просмотр засчитан',
            'view_count': video.video_views.count()  # здесь view_count считается по связке
        }

    except Video.DoesNotExist:
        return {'error': 'Видео не найдено'}
    except User.DoesNotExist:
        return {'error': 'Пользователь не найден'}
        

@shared_task
def increment_view_count(video_id, user_id=None):
    Увеличивает счётчик просмотров видео и рейтинг, если пользователь ещё не смотрел 
    from videos.models import Video, VideoView, User
    from django.db.models import F

    try:
        video = Video.objects.get(id=video_id)
        user = User.objects.get(id=user_id) if user_id else None

        # Проверка: есть ли уже просмотр
        obj, created = VideoView.objects.get_or_create(video=video, user=user)

        if created:
            # Только если новый просмотр — увеличиваем просмотры и рейтинг
            Video.objects.filter(id=video_id).update(
                view_count=F('view_count') + 1,
                rating=F('rating') + 1
            )

        # Обновим объект и вернём актуальное значение
        video.refresh_from_db()
        return {
            'message': 'Просмотр засчитан',
            'view_count': video.view_count
        }

    except Video.DoesNotExist:
        return {'error': 'Видео не найдено'}
    except User.DoesNotExist:
        return {'error': 'Пользователь не найден'}
        



@shared_task
def increment_view_count(video_id, user_id=None):
    from videos.models import Video, VideoView, User

    try:
        video = Video.objects.get(id=video_id)
        user = User.objects.get(id=user_id) if user_id else None

        # Проверим, не существует ли уже просмотр
        obj, created = VideoView.objects.get_or_create(video=video, user=user)

        if created:
            # Только при новом просмотре увеличиваем счётчики
            Video.objects.filter(id=video_id).update(
                view_count=F('view_count') + 1,
                rating=F('rating') + 1
            )
            video.refresh_from_db()  # <--- добавлено
            return {'message': 'Просмотр засчитан', 'view_count': video.view_count}
        else:
            return {'message': 'Уже засчитан ранее', 'view_count': video.view_count}

    except Video.DoesNotExist:
        return {'error': 'Видео не найдено'}
    except User.DoesNotExist:
        return {'error': 'Пользователь не найден'}
        


@shared_task
def increment_view_count(video_id, user_id=None):
    from videos.models import Video, VideoView, User

    try:
        video = Video.objects.get(id=video_id)
        user = User.objects.get(id=user_id) if user_id else None

        # Проверим, не существует ли уже просмотр
        obj, created = VideoView.objects.get_or_create(video=video, user=user)

        if created:
            # Только при новом просмотре увеличиваем оба поля
            Video.objects.filter(id=video_id).update(
                view_count=F('view_count') + 1,
                rating=F('rating') + 1
            )
            return {'message': 'Просмотр засчитан', 'view_count': video.view_count + 1}
        else:
            return {'message': 'Уже засчитан ранее', 'view_count': video.view_count}

    except Video.DoesNotExist:
        return {'error': 'Видео не найдено'}
    except User.DoesNotExist:
        return {'error': 'Пользователь не найден'}
        


@shared_task
def increment_view_count(video_id, user_id=None):
     Увеличивает счётчик просмотров видео асинхронно и создаёт запись VideoView 
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
    