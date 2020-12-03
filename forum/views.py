from django.shortcuts import render,redirect
import cx_Oracle
from django.urls import reverse
# Create your views here.

def main(request):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    userid = request.session['userid']
    role = request.session['role']

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()
    statement = """SELECT F.ID,F.TOPIC,F.QUESTION_DESCRIPTION,C.NAME,C.CLASS,S.NAME,A1.ANSWER_DESCRIPTION
                FROM FORUM_QUES F,COURSES C,USERS S,FORUM_ANS A1
                WHERE C.ID = F.COURSE_ID AND S.ID = F.ST_ID AND A1.FORUM_ID(+) = F.ID
                AND A1.ANS_TIME>=ALL(SELECT FA.ANS_TIME FROM FORUM_ANS FA WHERE FA.FORUM_ID = F.ID)"""
    c.execute(statement)
    forumset = c.fetchall()
    if forumset != []:
        print(forumset)
  

    
    return render(request,'forum/forum.html',{'userid':userid,'role':role,'forumset':forumset})

def post_comment(request,video_id):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        role= request.session['role']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor() 

    if request.method == 'POST' :
        statement="""
                    INSERT INTO VIDEO_COMMENTS
                    VALUES(1,NULL,:0,:1,:2,sysdate)
                    """
        text=request.POST['comment_text']
        print(text)
        c.execute(statement,(video_id,userid,text))
    connection.commit()

    c.close()
    connection.close()

    return redirect('/courses/course_contents/video/'+str(video_id))
