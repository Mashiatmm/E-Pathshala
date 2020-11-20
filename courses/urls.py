from django.urls import path
from . import views

app_name='courses'

urlpatterns = [
        path('add_course/',views.add_course,name='add_course'),
        path('course_contents/teacher/<int:course_id>/',views.course_contents,name='course_contents'),
        path('add_content/<int:course_id>/<int:topic_id>/',views.add_content,name='add_content'),
        path('topic_details/<int:topic_id>/',views.topic_details,name='topic_details'),
        path('topic_update/<int:topic_id>/',views.update_topic,name='topic_update'),
        path('add_exams/<int:course_id>/<int:topic_id>/',views.add_exams,name='add_exams'),
        path('add_ques/<int:exam_id>/',views.add_ques,name='add_ques'),
        path('del_ques/<int:exam_id>/<int:ques_id>/',views.del_ques,name='del_ques'),
        path('edit_ques/<int:exam_id>/<int:ques_id>/',views.edit_ques,name='edit_ques'),
        path('enroll_course/',views.enroll_course,name='enroll_course'),
        path('all_courses/student/<int:id>',views.all_courses_student,name='all_courses_student'),
        path('course_contents/student/<int:topic_id>',views.course_contents_student,name='course_contents_student'),
        path('course_topics/student/<int:course_id>',views.course_topics_student,name='course_topics_student'),
]
