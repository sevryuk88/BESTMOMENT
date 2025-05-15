# pushapp/urls.py

from django.urls import path
from pushapp import views

app_name = 'webpush'

urlpatterns = [
    path('subscribe/', views.save_info_view, name='subscribe'),
    path('send_push/', views.send_push, name='send_push'),
]
