
# videos/models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import F
from datetime import timedelta
#from videos.tasks import update_video_rating
import videos.tasks  # Не вызываем импорт конкретной функции
from storages.backends.s3boto3 import S3Boto3Storage

s3_storage = S3Boto3Storage()
  

User = get_user_model()

# ✅ Менеджер для публикаций
class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

# ✅ Видео-модель
class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/', storage=s3_storage)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='videos', null=True, default=None)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='category', null=True, blank=True)  
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    rating = models.IntegerField(default=0)

    objects = models.Manager()
    published = PublishedModel()

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
            models.Index(fields=['rating']),
            models.Index(fields=['likes', 'dislikes']),  # ✅ Вместо index_together
            models.Index(fields=['time_create', 'rating']),  # ✅ Вместо index_together
        ]
   
    
    def __str__(self):
        return self.title
    
    @property
    def likes_count(self):
        return self.votes.filter(is_like=True).count()

    @property
    def dislikes_count(self):
        return self.votes.filter(is_like=False).count()

    @property
    def view_count(self):
        return self.video_views.count()

    def get_view_count(self):
        return self.video_views.count()

    #  Перенесём обновление рейтинга в Celery (уменьшим нагрузку)
    def update_rating(self):
        #update_video_rating.delay(self.id)
        videos.tasks.update_video_rating.delay(self.id)
        

#  Категории видео
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('videos:category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

#  Комментарии
class Comment(models.Model):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.video.title}'

#  Голосование (лайки/дизлайки)
class Vote(models.Model):
    video = models.ForeignKey('Video', related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField()

    class Meta:
        unique_together = ('video', 'user')

    def __str__(self):
        return f"{self.user.username} voted {'like' if self.is_like else 'dislike'} on {self.video.title}"

#  Просмотры
class VideoView(models.Model):
    video = models.ForeignKey('Video', related_name='video_views', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Поддержка анонимных пользователей

    class Meta:
        unique_together = ('video', 'user')

    def __str__(self):
        return f"View of {self.video.title} by {self.user.username if self.user else 'Anonymous'}"

#  Избранные видео
class FavoriteVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_videos')
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user.username} added {self.video.title} to favorites"
      