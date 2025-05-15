#users/views 


from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm, CustomPasswordResetForm
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
         
from videos.models import Video, Comment, FavoriteVideo, Vote
from django.db.models import Count, Sum, Q

from django.shortcuts import render, get_object_or_404  # <--- не забудь импорт
from django.views import View
from .models import User  # если используется кастомная модель





User = get_user_model()





class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}
    
    
   
    
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')
    
    
    
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm

    
    

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя", 'default_image': settings.DEFAULT_USER_IMAGE}
    
        
 
    def get_success_url(self):
        return reverse_lazy('users:profile')
        
        
    def get_object(self, queryset=None):
        return self.request.user
        
  
    
    def form_valid(self, form):
    # Проверка, была ли нажата кнопка удаления фото
        if 'delete_photo' in self.request.POST:
            self.object.photo.delete(save=False)
            self.object.photo = None
            self.object.save()
            return redirect(self.get_success_url())

    # Если просто форма сохранения
        response = super().form_valid(form)

    # Если загружено новое фото
        if 'photo' in self.request.FILES:
            self.object.photo = self.request.FILES['photo']
            self.object.save()

        return response
    

        
                                
    
class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}
    

       
        
# ✅ Таблица лидеров пользователей
def leaderboard_view(request):
    selected_user_id = request.GET.get('user_id')  # <-- Добавляем эту строчку

    users = User.objects.annotate(
        total_likes=Count('vote', filter=Q(vote__is_like=True)),
        total_comments=Count('comment'),
        total_favorites=Count('favorite_videos'),
        score=Sum('videos__rating')
    ).order_by('-total_likes')  # СОРТИРУЕМ по total_likes

    return render(request, 'users/leaderboard.html', {
        'users': users,
        'selected_user_id': int(selected_user_id) if selected_user_id else None  # <-- И добавляем сюда
    })
    
    
    



class OtherUserProfileView(LoginRequiredMixin, View):
    def get(self, request, username):
        profile_user = get_object_or_404(User, username=username)
        is_owner = request.user == profile_user
        is_subscriber = profile_user.subscribers.filter(id=request.user.id).exists()

        my_videos = Video.objects.filter(author=profile_user).order_by('-uploaded_at')
        favorite_videos = FavoriteVideo.objects.filter(user=profile_user).select_related('video')

        return render(request, 'videos/my_videos.html', {
            'profile_user': profile_user,
            'is_owner': is_owner,
            'is_subscriber': is_subscriber,
            'my_videos': my_videos,
            'favorite_videos': [f.video for f in favorite_videos],
            'vapid_public_key': settings.WEBPUSH_SETTINGS['VAPID_PUBLIC_KEY'],  # ✅ добавь ЭТО
            
        })
        
        

@login_required
def toggle_subscription(request, username):
    profile_user = get_object_or_404(User, username=username)
    if profile_user != request.user:
        if request.user in profile_user.subscribers.all():
            profile_user.subscribers.remove(request.user)
        else:
            profile_user.subscribers.add(request.user)
    return redirect('users:other_profile', username=profile_user.username)
    


@login_required
def my_videos_view(request):
    profile_user = request.user
    my_videos = Video.objects.filter(author=profile_user).order_by('-uploaded_at')
    favorite_videos = FavoriteVideo.objects.filter(user=profile_user).select_related('video')

    return render(request, 'videos/my_videos.html', {
        'profile_user': profile_user,
        'is_owner': True,
        'is_subscriber': True,  # ← важно
        'my_videos': my_videos,
        'favorite_videos': [f.video for f in favorite_videos],
        'vapid_public_key': settings.WEBPUSH_SETTINGS['VAPID_PUBLIC_KEY'],  # ← вот эта строка
        
    })
    