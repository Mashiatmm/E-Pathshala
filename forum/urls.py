from django.urls import path
from . import views

app_name='forum'

urlpatterns = [
   path('main/',views.main,name='main'),
   path('post_comment/<int:video_id>',views.post_comment,name='post_comment')
    
]