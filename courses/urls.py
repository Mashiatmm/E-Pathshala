from django.urls import path
from . import views

app_name='courses'

urlpatterns = [
        path('add_course/',views.add_course,name='add_course'),
        path('edit_course/<int:course_id>/',views.edit_course,name='edit_course'),
        path('del_course/<int:course_id>/',views.del_course,name='del_course'),
        path('course_contents/teacher/<int:course_id>/',views.course_contents,name='course_contents'),
        path('add_content/<int:course_id>/<int:topic_id>/',views.add_content,name='add_content'),
        path('modify_content/<int:topic_id>/<content_type>/<int:content_id>/',views.modify_content,name='modify_content'),
        path('del_content/<int:topic_id>/<int:content_id>/',views.del_content,name='del_content'),
        path('content_serial/<type>/<int:sl_no>/<int:content_id>/<int:topic_id>/',views.content_serial,name='content_serial'),
        path('topic_details/<int:topic_id>/',views.topic_details,name='topic_details'),
        path('topic_update/<int:topic_id>/',views.update_topic,name='topic_update'),
        path('del_topic/<int:course_id>/<int:topic_id>/',views.del_topic,name='del_topic'),
        path('topic_serial/<type>/<int:sl_no>/<int:topic_id>/<int:course_id>',views.topic_serial,name='topic_serial'),
        path('add_exams/<int:course_id>/<int:topic_id>/',views.add_exams,name='add_exams'),
        path('add_ques/<int:exam_id>/',views.add_ques,name='add_ques'),
        path('del_ques/<int:exam_id>/<int:ques_id>/',views.del_ques,name='del_ques'),
        path('edit_ques/<int:exam_id>/<int:ques_id>/',views.edit_ques,name='edit_ques'),

        path('enroll_course/',views.enroll_course,name='enroll_course'),
        path('all_courses',views.all_courses,name='all_courses'),
        path('course_contents/student/<int:topic_id>',views.course_contents_student,name='course_contents_student'),
        path('course_topics/student/<int:course_id>',views.course_topics_student,name='course_topics_student'),
        path('course_contents/video/<int:content_id>',views.show_video,name='show_video'),
        path('course_contents/exam/<int:content_id>',views.give_exam,name='give_exam'),

        path('next_content/student/<int:content_id>',views.next_content_student,name='next_content_student'),

]
