from django.urls import path
from . import views

app_name='courses'

urlpatterns = [
        path('add_course/<int:id>/',views.add_course,name='add_course'),
        path('all_courses/<int:id>/',views.all_courses,name='all_courses'),
        path('course_contents/<int:course_id>/',views.course_contents,name='course_contents'),
        path('add_content/<int:course_id>/<int:topic_id>/',views.add_content,name='add_content'),
        path('add_exams/<int:course_id>/<int:topic_id>/',views.add_exams,name='add_exams'),
]
