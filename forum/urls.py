from django.urls import path
from . import views

app_name='forum'

urlpatterns = [
   path('main/',views.main,name='main'),
    
]