#video/forms.py
from django import forms
from .models import Video, Comment
from django.core.exceptions import ValidationError

# Функция для валидации формата и размера видео
def validate_video_file(value):
    if not value.name.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise ValidationError('The file must be in MP4 or MOV format.')
    if value.size > 500 * 1024 * 1024:  # 500MB
        raise ValidationError('The file size should not exceed 500MB.')

# Форма для загрузки видео 
class VideoForm(forms.ModelForm):
    video_file = forms.FileField(
        label="Выберите видео",
        validators=[validate_video_file],
        widget=forms.ClearableFileInput(attrs={'class': 'form-input'})
    )
    
    
    title = forms.CharField(
        max_length=100,
        label="Video Title",
        widget=forms.TextInput(attrs={
            'class': 'title-input',
            'placeholder': "Free kick goal by Mess",
        })
    )

    class Meta:
        model = Video
        fields = ['title']

# Форма для комментариев
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Введите комментарий...',
                'rows': 2,
                'class': 'comment-textarea'
            }),
        }


