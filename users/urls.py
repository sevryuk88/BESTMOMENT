#users/urls
from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView,  PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
from .views import CustomPasswordResetView  # Импорт кастомного представления
from django.urls import reverse, reverse_lazy
from .views import my_videos_view, leaderboard_view, toggle_subscription



app_name = "users"
 
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  
    
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name='password_change_done'),
      
    #PasswordResetView  
    path('password-reset/',
         CustomPasswordResetView.as_view(
             template_name="users/password_reset_form.html",
             email_template_name="users/password_reset_email.html",
             success_url=reverse_lazy("users:password_reset_done")
         ),
         name='password_reset'),
         
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name = "users/password_reset_done.html"),
         name='password_reset_done'),                 
         
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="users/password_reset_confirm.html",
             success_url=reverse_lazy("users:password_reset_complete")
         ),
         name='password_reset_confirm'),

                  
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name='password_reset_complete'),
           
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    
    path('profile/<str:username>/', views.OtherUserProfileView.as_view(), name='other_profile'),
    
    path('toggle-subscription/<str:username>/', views.toggle_subscription, name='toggle_subscription'),
    
    
    path('my-videos/', my_videos_view, name='my_videos'),

    
    
       

]