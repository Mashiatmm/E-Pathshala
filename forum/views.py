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
    statement = """SELECT F.ID,F.TOPIC,F.QUESTION_DESCRIPTION,F.QUESTION_TIME,C.NAME,C.CLASS,S.NAME
                FROM FORUM_QUES F,COURSES C,USERS S
                WHERE C.ID = F.COURSE_ID AND S.ID = F.ST_ID """
    c.execute(statement)
    forumset = c.fetchall()
   
    return render(request,'forum/forum.html',{'userid':userid,'role':role,'forumset':forumset})