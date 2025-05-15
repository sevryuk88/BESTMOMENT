#video/templatetags/video_tags.py
from django import template
import videos.views as views
from videos.models import Category
from django.db.models.functions import Length



register = template.Library()

  
@register.inclusion_tag('videos/rubric.html')
def show_categories():
    cats = Category.objects.annotate(name_length=Length('name')).order_by('-name_length')
    
    return {"cats": cats}
    