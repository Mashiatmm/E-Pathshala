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
    statement = """SELECT F.ID,F.TOPIC,F.QUESTION_DESCRIPTION,F.QUESTION_TIME,C.NAME,C.CLASS,S.NAME,
                (SELECT COUNT(*) FROM FORUM_ANS WHERE FORUM_ID = F.ID)
                FROM FORUM_QUES F,COURSES C,USERS S
                WHERE C.ID(+) = F.COURSE_ID AND S.ID = F.ST_ID 
                ORDER BY F.QUESTION_TIME DESC"""
    c.execute(statement)
    forumset = c.fetchall()
    statement = "SELECT NAME,CLASS,ID FROM COURSES"
    c.execute(statement)
    courses = c.fetchall()
    #print(forumset)
    c.close()
    connection.close()
    return render(request,'forum/forum.html',{'userid':userid,'role':role,'forumset':forumset,'courses':courses})

def addForumQues(request):
    st_id = request.session['userid']
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()
    
    statement = """INSERT INTO FORUM_QUES(ID,TOPIC,ST_ID,QUESTION_DESCRIPTION,QUESTION_TIME)
                     VALUES(0,:0,:1,:2,SYSDATE)"""
    c.execute(statement,(request.POST['topic'],st_id,request.POST['description']))

    connection.commit()
    c.close()
    connection.close()
    return redirect('/forum/main')


def searchForum(request):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    userid = request.session['userid']
    role = request.session['role']

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()
    searchkey = request.POST['SearchKey'].lower()
    statement = """SELECT F.ID,F.TOPIC,F.QUESTION_DESCRIPTION,F.QUESTION_TIME,C.NAME,C.CLASS,S.NAME,
                    (SELECT COUNT(*) FROM FORUM_ANS WHERE FORUM_ID = F.ID)
                    FROM FORUM_QUES F,COURSES C,USERS S
                    WHERE C.ID(+) = F.COURSE_ID AND S.ID = F.ST_ID 
                    AND F.ID = ANY(SELECT FF.ID FROM FORUM_QUES FF
                    WHERE LOWER(FF.TOPIC) LIKE :s OR LOWER(FF.QUESTION_DESCRIPTION) LIKE :s)
                    ORDER BY F.QUESTION_TIME DESC"""
    
    c.execute(statement,{'s':'%'+searchkey+'%'})
    forumset = c.fetchall()
    #print(forumset)

    statement = "SELECT NAME,CLASS,ID FROM COURSES"
    c.execute(statement)
    courses = c.fetchall()

    c.close()
    connection.close()
    return render(request,'forum/forum.html',{'userid':userid,'role':role,'forumset':forumset,'courses':courses})

def sortbyUnanswered(request):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    userid = request.session['userid']
    role = request.session['role']

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()
    statement = """SELECT F.ID,F.TOPIC,F.QUESTION_DESCRIPTION,F.QUESTION_TIME,C.NAME,C.CLASS,S.NAME,
                    (SELECT COUNT(*) FROM FORUM_ANS WHERE FORUM_ID = F.ID)
                    FROM FORUM_QUES F,COURSES C,USERS S
                    WHERE C.ID(+) = F.COURSE_ID AND S.ID = F.ST_ID 
                    AND 0 = (SELECT COUNT(*) FROM FORUM_ANS WHERE FORUM_ID = F.ID)
                    ORDER BY F.QUESTION_TIME DESC"""
    c.execute(statement)
    forumset = c.fetchall()
    #print(forumset)

    statement = "SELECT NAME,CLASS,ID FROM COURSES"
    c.execute(statement)
    courses = c.fetchall()

    c.close()
    connection.close()
    return render(request,'forum/forum.html',{'userid':userid,'role':role,'forumset':forumset,'courses':courses})

def addForumAns(request,forum_id):
    user_id = request.session['userid']
    
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()
    
    statement = """INSERT INTO FORUM_ANS
                VALUES(:0,0,:1,:2,SYSDATE)"""
    c.execute(statement,(forum_id,user_id,request.POST['comment']))
    connection.commit()
    c.close()
    connection.close()
    return redirect('/forum/main')

def ques_details(request,forum_id):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    userid = request.session['userid']
    role = request.session['role']

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()

    statement = "SELECT A.FORUM_ID,U.NAME,A.ANSWER_DESCRIPTION,A.ANS_TIME,A.ID FROM FORUM_ANS A,USERS U WHERE A.FORUM_ID = :i AND U.ID = A.PUBLISHER_ID ORDER BY A.ANS_TIME DESC"
    c.execute(statement,{'i':forum_id})
    ReplySet = c.fetchall()

    statement = """SELECT F.ID,F.TOPIC,F.QUESTION_DESCRIPTION,F.QUESTION_TIME,C.NAME,C.CLASS,S.NAME
                    FROM FORUM_QUES F,COURSES C,USERS S
                    WHERE F.ID = :i AND C.ID(+) = F.COURSE_ID AND S.ID = F.ST_ID"""
    
    c.execute(statement,{'i':forum_id})
    QuestionDetails = c.fetchone()
    c.close()
    connection.close()

    return render(request,'forum/question.html',{'userid':userid,'role':role,'ReplySet':ReplySet,'QuesDetails':QuestionDetails})

def upvote(request,forum_id,forum_ans_id):
    userid = request.session['userid']
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()

    try:
        statement = """INSERT INTO VOTE
                    VALUES(:0,:1,:2)"""
        c.execute(statement,(forum_id,forum_ans_id,userid))
    except Exception as e:
        print(e)
        statement = """DELETE FROM VOTE
                    WHERE FORUM_ID = :f AND FORUM_ANS_ID = :a AND USER_ID = :u"""
        c.execute(statement,{'f':forum_id,'a':forum_ans_id,'u':userid})
    connection.commit()
    c.close()
    connection.close()
    return redirect('/forum/ques_details/'+str(forum_id))


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

def post_reply(request,parent_id):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        role= request.session['role']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()  
    if request.method == 'POST' :

        text=request.POST['reply_text']
        print(text)
        statement="SELECT VIDEO_ID FROM VIDEO_COMMENTS WHERE ID = :parent_id"
        c.execute(statement,{'parent_id':parent_id})
        video_id,= c.fetchone()
        if text:
            
            statement="""
                        INSERT INTO VIDEO_COMMENTS
                        VALUES(1,:0,:1,:2,:3,sysdate)
                        """
        
            c.execute(statement,(parent_id,video_id,userid,text))  
        request.session['parent_comment_id'] = parent_id

    connection.commit()

    c.close()
    connection.close()

    return redirect('/courses/course_contents/video/'+str(video_id))


def show_reply(request,parent_id):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        role= request.session['role']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    request.session['parent_comment_id']=parent_id

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()  
    statement="SELECT VIDEO_ID FROM VIDEO_COMMENTS WHERE ID = :parent_id"
    c.execute(statement,{'parent_id':parent_id})
    video_id,= c.fetchone()
    connection.commit()

    c.close()
    connection.close()

    return redirect('/courses/course_contents/video/'+str(video_id))


"""
<select class="custom-select" id="course" name="course" placeholder = "Select Course">
                      
                      <option>No Course</option>
                      {% for course in courses %}
                        <option value="{{course.2}}">{{course.0}},Class {{course.1}}</option>
                      {% endfor %}
                      
                    </select>
                    
                    <br><br>
"""