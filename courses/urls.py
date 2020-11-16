from django.urls import path
from . import views

app_name='courses'

urlpatterns = [
        path('add_course/<int:id>/',views.add_course,name='add_course'),
        path('all_courses/teacher/<int:id>/',views.all_courses,name='all_courses'),
        path('enroll_course/',views.enroll_course,name='enroll_course'),
        path('all_courses/student/<int:id>',views.all_courses_student,name='all_courses_student'),
        path('course_contents/<int:course_id>/',views.course_contents,name='course_contents'),
        path('add_content/<int:course_id>/<int:topic_id>/',views.add_content,name='add_content'),
        path('add_exams/<int:course_id>/<int:topic_id>/',views.add_exams,name='add_exams'),
        path('add_ques/<int:exam_id>/',views.add_ques,name='add_ques'),
]
