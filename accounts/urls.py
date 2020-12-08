from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('signup/<role>',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('profile',views.profile,name='profile'),
    path('settings',views.settings,name = 'settings'),
    path('students',views.students,name = 'students'),
    path('progress',views.progress,name = 'progress'),
    path('course_classes',views.course_classes,name = 'course_classes'),
    path('person_profile/<int:id>',views.person_profile,name = 'person_profile'),
    path('notifications',views.notifications,name = 'notifications'),
    path('delete_notifications',views.delete_notifications,name = 'delete_notifications'),
    path('seen_notifications',views.seen_notifications,name = 'seen_notifications'),
    
    
    
]