#video/urls.py
from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('upload/', views.AddPage.as_view(), name='upload_video'),
    path('', views.VideoList.as_view(), name='video_list'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('comment/<int:video_id>/', views.AddCommentView.as_view(), name='add_comment'),
    path('like/', views.like_video, name='like_video'),
    path('dislike/', views.dislike_video, name='dislike_video'),
    path('record-view/', views.record_video_view, name='record_view'),
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('my-videos/', views.MyVideosView.as_view(), name='my_videos'),
  
    #path('search/', views.search_videos, name='search_videos'),

]


