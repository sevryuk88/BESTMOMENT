from django.contrib import admin
from .models import Video, Category, Comment, Vote, VideoView, FavoriteVideo
from django.utils.html import format_html
from django.contrib.auth import get_user_model

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.sites import AlreadyRegistered


User = get_user_model()

# =========================
# Inline для комментариев
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("author", "content", "created_at")


# =========================
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'is_approved', 'uploaded_at',
        'likes_display', 'dislikes_display', 'rating', 'view_count_display'
    )
    list_display_links = ('id', 'title')
    list_filter = ('is_approved', 'is_published', 'cat', 'uploaded_at')
    search_fields = ('title', 'author__username')
    actions = ['approve_videos']
    inlines = [CommentInline]
    readonly_fields = (
        'uploaded_at', 'time_create', 'time_update',
        'likes', 'dislikes', 'rating', 'view_count_display'
    )
    autocomplete_fields = ('author', 'cat')

    def approve_videos(self, request, queryset):
        queryset.update(is_approved=True)
    approve_videos.short_description = "✅ Одобрить выбранные видео"

    def likes_display(self, obj):
        return obj.likes_count
    likes_display.short_description = "Лайки"

    def dislikes_display(self, obj):
        return obj.dislikes_count
    dislikes_display.short_description = "Дизлайки"

    def view_count_display(self, obj):
        return obj.view_count
    view_count_display.short_description = "Просмотры"


# =========================
@admin.register(FavoriteVideo)
class FavoriteVideoAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'added_at')
    search_fields = ('user__username', 'video__title')


# =========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)  # ✅ Обязательно для autocomplete_fields


# =========================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'author', 'short_content', 'created_at')
    list_display_links = ('id', 'video')
    search_fields = ('author__username', 'video__title', 'content')
    list_filter = ('created_at',)

    def short_content(self, obj):
        return obj.content[:40] + "..." if len(obj.content) > 40 else obj.content
    short_content.short_description = "Комментарий"


# =========================
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'is_like')
    list_filter = ('is_like',)
    search_fields = ('user__username', 'video__title')


# =========================
@admin.register(VideoView)
class VideoViewAdmin(admin.ModelAdmin):
    list_display = ('video', 'user')
    
    
# Перерегистрируем модель User с новыми настройками
try:
    admin.site.unregister(User)
except AlreadyRegistered:
    pass


# =========================
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'updated_at', 'subscriber_count')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'updated_at')
    filter_horizontal = ('subscribers',)

    def subscriber_count(self, obj):
        return obj.subscribers.count()
    subscriber_count.short_description = "Кол-во подписчиков"
    