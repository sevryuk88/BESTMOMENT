# urls.py (проект)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('grappelli/', include('grappelli.urls')),
  
    path('admin/', admin.site.urls),  
    path('', include('videos.urls', namespace='videos')),      
    path('users/', include('users.urls', namespace="users")),  
    path('accounts/', include('django.contrib.auth.urls')),  # Встроенные маршруты Django
    path('webpush/', include('pushapp.urls', namespace='webpush')),
    
]

# Подключение статики и медиа в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Настройки административной панели
admin.site.site_header = "Панель администратора"
admin.site.index_title = "BESTMOMENTS"











       