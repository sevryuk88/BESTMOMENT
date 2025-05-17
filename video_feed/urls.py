# urls.py (проект)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth import get_user_model

# Временная функция для применения миграций
def run_migrations(request):
    call_command("migrate")
    return HttpResponse("✅ Migrations applied.")

# Временная функция для создания суперпользователя
def create_admin_user(request):
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "adminpass123")
        return HttpResponse("✅ Superuser created.")
    else:
        return HttpResponse("⚠️ Superuser already exists.")


urlpatterns = [
    #path('grappelli/', include('grappelli.urls')),
  
    path('admin/', admin.site.urls),  
    path('', include('videos.urls', namespace='videos')),      
    path('users/', include('users.urls', namespace="users")),  
    path('accounts/', include('django.contrib.auth.urls')),  # Встроенные маршруты Django
    path('webpush/', include('pushapp.urls', namespace='webpush')),
    
    path('run-migrations/', run_migrations),     # временный путь
    path('create-admin/', create_admin_user),    # временный путь
    
    
]

# Подключение статики и медиа в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Настройки административной панели
admin.site.site_header = "Панель администратора"
admin.site.index_title = "BESTMOMENTS"











       