from django.urls import path
from . import views

app_name='forum'

urlpatterns = [
   path('main/',views.main,name='main'),
   path('searchForum/',views.searchForum,name='searchForum'),
   path('sortByUnanswered/',views.sortbyUnanswered,name='sortByUnanswered'),
   path('sortByTop/',views.sortByTop,name='sortByTop'),
   path('addForumQues/',views.addForumQues,name='addForumQues'),
   path('addForumAns/<int:forum_id>/<page>',views.addForumAns,name='addForumAns'),
   path('ques_details/<int:forum_id>',views.ques_details,name='ques_details'),
   path('quesSortByVotes/<int:forum_id>',views.quesSortByVotes,name='quesSortByVotes'),
   path('ques_edit/<int:forum_id>',views.ques_edit,name='ques_edit'),
   path('ans_edit/<int:forum_ans_id>',views.ans_edit,name='ans_edit'),
   path('ques_del/<int:forum_id>',views.ques_del,name='ques_del'),
   path('ans_del/<int:forum_ans_id>',views.ans_del,name='ans_del'),
   path('upvote/<int:forum_id>/<int:forum_ans_id>',views.upvote,name='upvote'),
   path('activity/',views.activity,name='activity'),
   path('post_comment/<int:video_id>',views.post_comment,name='post_comment'),
   path('post_reply/<int:parent_id>',views.post_reply,name='post_reply'),
   path('show_reply/<int:parent_id>',views.show_reply,name='show_reply'),
    
]