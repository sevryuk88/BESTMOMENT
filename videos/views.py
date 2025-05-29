#videos/views 
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView, TemplateView
from django.views import View
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from django.db.models import F
from .models import Video, Category, Vote, VideoView, FavoriteVideo
from .forms import VideoForm, CommentForm
from .tasks import increment_view_count  # Celery-задача для просмотров
from django.utils.timezone import localtime
from django.contrib import messages  # ← добавь это
from utils.telegram_notify import send_telegram_message
from django.db.models import Q
from django.templatetags.static import static




class AddPage(LoginRequiredMixin, FormView):
    form_class = VideoForm
    template_name = 'videos/upload_video.html'
    success_url = reverse_lazy('videos:video_list')

    def form_valid(self, form):
        video = form.save(commit=False)
        video.author = self.request.user

        uploaded_file = self.request.FILES.get('video_file')
        if uploaded_file:
            video.video_file = uploaded_file
            video.save()
        else:
            form.add_error('video_file', "Файл не загружен")
            return self.form_invalid(form)

        messages.info(self.request, "Ваше видео отправлено на модерацию.")
        send_telegram_message(
            f"📹 <b>Новое видео от {self.request.user.username}</b>\nОжидает модерации в админке."
        )
        return super().form_valid(form)
              
  
      
def get_top_videos():
    top_video_ids = cache.get('top_videos')

    if not top_video_ids:
        ten_days_ago = timezone.now() - timedelta(days=10)
        top_videos = Video.objects.filter(time_create__gte=ten_days_ago).order_by('-rating')[:10]
        top_video_ids = [video.id for video in top_videos]
        cache.set('top_videos', top_video_ids, timeout=864000)

    return Video.objects.filter(id__in=top_video_ids).select_related('author').prefetch_related('comments').order_by('-rating')
    



class VideoList(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'videos/video_list.html'

    def get_queryset(self):
        queryset = Video.objects.filter(is_approved=True).select_related('author').prefetch_related('comments')

        filter_top10 = self.request.GET.get('top10', 'false')
        if filter_top10 == 'true':
            return get_top_videos()

        return queryset
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        videos = self.get_queryset()

        for video in videos:
            video.user_liked = video.votes.filter(user=self.request.user, is_like=True).exists()
            video.user_disliked = video.votes.filter(user=self.request.user, is_like=False).exists()

        context['videos'] = videos
        context['top10'] = self.request.GET.get('top10', 'false')

        # ✅ Добавляем список ID избранных видео пользователя
        if self.request.user.is_authenticated:
            favorite_ids = set(
                FavoriteVideo.objects.filter(user=self.request.user).values_list('video_id', flat=True)
            )
        else:
            favorite_ids = set()

        context['user_favorites'] = favorite_ids

        return context
    

    


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    videos = Video.objects.filter(cat_id=category.pk)
    return render(request, 'videos/video_list.html', {'title': f'Рубрика: {category.name}', 'videos': videos})





class AddCommentView(View):
    def post(self, request, video_id):
        video = get_object_or_404(Video, id=video_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.author = request.user
            comment.save()

            video.update_rating()

            # 🟢 Готовим URL аватарки
            
            if comment.author.photo:
                photo_url = comment.author.photo.url
                updated_at = comment.author.updated_at.timestamp()
                full_photo_url = f"{photo_url}?v={int(updated_at)}"
            else:
                full_photo_url = static('users/profil/user_main.jpeg')
    
            '''
            if comment.author.photo:
                photo_url = comment.author.photo.url
                updated_at = comment.author.photo.updated_at.timestamp() if hasattr(comment.author.photo, 'updated_at') else ''
                full_photo_url = f"{photo_url}?v={int(updated_at)}" if updated_at else photo_url
            else:
                full_photo_url = '/media/users/user.png'
            '''

            return JsonResponse({
                'content': comment.content,
                'author': comment.author.username,
                'created_at': localtime(comment.created_at).strftime('%d.%m.%Y %H:%M'),
                'photo_url': full_photo_url  # 🔥 вот оно!
            })

        return JsonResponse({'error': 'Форма не валидна'}, status=400)


@require_POST
def like_video(request):
    video_id = request.POST.get('video_id')
    video = get_object_or_404(Video, id=video_id)

    vote, created = Vote.objects.get_or_create(video=video, user=request.user, defaults={'is_like': True})

    if not created and not vote.is_like:
        vote.is_like = True
        vote.save(update_fields=['is_like'])

    if created:
        Video.objects.filter(id=video_id).update(rating=F('rating') + 2)

    video = Video.objects.get(id=video_id)

    return JsonResponse({
        'likes': video.likes_count,
        'dislikes': video.dislikes_count,
        'rating': video.rating,
        'views': video.view_count,
        'comments': video.comments.count()
    })


@require_POST
def dislike_video(request):
    video_id = request.POST.get('video_id')
    video = get_object_or_404(Video, id=video_id)

    vote, created = Vote.objects.get_or_create(video=video, user=request.user, defaults={'is_like': False})

    if not created and vote.is_like:
        vote.is_like = False
        vote.save(update_fields=['is_like'])

    if created:
        Video.objects.filter(id=video_id).update(rating=F('rating') - 2)

    video = Video.objects.get(id=video_id)

    return JsonResponse({
        'likes': video.likes_count,
        'dislikes': video.dislikes_count,
        'rating': video.rating,
        'views': video.view_count,
        'comments': video.comments.count()
    })
    

@require_POST
def record_video_view(request):
    video_id = request.POST.get('video_id')
    if not video_id:
        return JsonResponse({'error': 'Не указан идентификатор видео.'}, status=400)

    user_id = request.user.id if request.user.is_authenticated else None
    increment_view_count.delay(video_id, user_id)

    return JsonResponse({'message': 'Просмотр засчитан'})
    

"""
@require_POST
def record_video_view(request):
    video_id = request.POST.get('video_id')
    if not video_id:
        return JsonResponse({'error': 'Не указан идентификатор видео.'}, status=400)

    increment_view_count.delay(video_id)

    return JsonResponse({'message': 'Просмотр засчитан'})
"""

@require_POST
def toggle_favorite(request):
    video_id = request.POST.get('video_id')
    video = get_object_or_404(Video, id=video_id)

    favorite, created = FavoriteVideo.objects.get_or_create(user=request.user, video=video)

    if created:
        is_favorited = True
    else:
        favorite.delete()
        is_favorited = False

    return JsonResponse({'is_favorited': is_favorited})


class MyVideosView(LoginRequiredMixin, TemplateView):
    template_name = "videos/my_videos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_videos'] = Video.objects.filter(author=self.request.user, is_approved=True)
        context['favorite_videos'] = Video.objects.filter(favorited_by__user=self.request.user)
        return context
        
        
        
    
        
        
        