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
    statement = """SELECT F.ID,F.TOPIC,F.QUESTION_DESCRIPTION,F.QUESTION_TIME,S.NAME,
                (SELECT COUNT(*) FROM FORUM_ANS WHERE FORUM_ID = F.ID)
                FROM FORUM_QUES F,USERS S
                WHERE S.ID = F.ST_ID 
                ORDER BY F.QUESTION_TIME DESC"""
    c.execute(statement)
    forumset = c.fetchall()
    
    #print(forumset)
    c.close()
    connection.close()
    return render(request,'forum/forum.html',{'userid':userid,'role':role,'forumset':forumset})

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
    statement = """SELECT F.ID,F.TOPIC,F.QUESTION_DESCRIPTION,F.QUESTION_TIME,S.NAME,
                    (SELECT COUNT(*) FROM FORUM_ANS WHERE FORUM_ID = F.ID)
                    FROM FORUM_QUES F,USERS S
                    WHERE S.ID = F.ST_ID 
                    AND F.ID = ANY(SELECT FF.ID FROM FORUM_QUES FF
                    WHERE LOWER(FF.TOPIC) LIKE :s OR LOWER(FF.QUESTION_DESCRIPTION) LIKE :s)
                    ORDER BY F.QUESTION_TIME DESC"""
    
    c.execute(statement,{'s':'%'+searchkey+'%'})
    forumset = c.fetchall()
    #print(forumset)

    c.close()
    connection.close()
    return render(request,'forum/forum.html',{'userid':userid,'role':role,'forumset':forumset})

def sortbyUnanswered(request):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    userid = request.session['userid']
    role = request.session['role']

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()
    statement = """SELECT F.ID,F.TOPIC,F.QUESTION_DESCRIPTION,F.QUESTION_TIME,S.NAME,
                    (SELECT COUNT(*) FROM FORUM_ANS WHERE FORUM_ID = F.ID)
                    FROM FORUM_QUES F,USERS S
                    WHERE S.ID = F.ST_ID 
                    AND 0 = (SELECT COUNT(*) FROM FORUM_ANS WHERE FORUM_ID = F.ID)
                    ORDER BY F.QUESTION_TIME DESC"""
    c.execute(statement)
    forumset = c.fetchall()
    #print(forumset)


    c.close()
    connection.close()
    return render(request,'forum/forum.html',{'userid':userid,'role':role,'forumset':forumset})

def sortByTop(request):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    userid = request.session['userid']
    role = request.session['role']

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()
    statement = """SELECT F.ID,F.TOPIC,F.QUESTION_DESCRIPTION,F.QUESTION_TIME,S.NAME,
                    (SELECT COUNT(*) FROM FORUM_ANS WHERE FORUM_ID = F.ID) AS REPLIES
                    FROM FORUM_QUES F,USERS S
                    WHERE S.ID = F.ST_ID 
                    ORDER BY REPLIES DESC"""
    c.execute(statement)
    forumset = c.fetchall()
    #print(forumset)

    c.close()
    connection.close()
    return render(request,'forum/forum.html',{'userid':userid,'role':role,'forumset':forumset})

def addForumAns(request,forum_id,page):
    user_id = request.session['userid']
    print(page)
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()
    
    statement = """INSERT INTO FORUM_ANS
                VALUES(:0,0,:1,:2,SYSDATE)"""
    c.execute(statement,(forum_id,user_id,request.POST['comment']))
    connection.commit()
    c.close()
    connection.close()
    if page == 'main':
        return redirect('/forum/main')
    else:
        return redirect('/forum/ques_details/'+str(forum_id))

def ques_details(request,forum_id):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    userid = request.session['userid']
    role = request.session['role']

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()

    statement = """SELECT A.FORUM_ID,U.NAME,A.ANSWER_DESCRIPTION,A.ANS_TIME,A.ID,
                    (SELECT COUNT(*) FROM VOTE WHERE FORUM_ID = A.FORUM_ID AND FORUM_ANS_ID = A.ID) AS VOTES
                    FROM FORUM_ANS A,USERS U 
                    WHERE A.FORUM_ID = :i AND U.ID = A.PUBLISHER_ID ORDER BY A.ANS_TIME DESC"""
    c.execute(statement,{'i':forum_id})
    ReplySet = c.fetchall()

    statement = """SELECT F.ID,F.TOPIC,F.QUESTION_DESCRIPTION,F.QUESTION_TIME,S.NAME
                    FROM FORUM_QUES F,USERS S
                    WHERE F.ID = :i AND S.ID = F.ST_ID"""
    
    c.execute(statement,{'i':forum_id})
    QuestionDetails = c.fetchone()
    c.close()
    connection.close()

    return render(request,'forum/question.html',{'userid':userid,'role':role,'ReplySet':ReplySet,'QuesDetails':QuestionDetails})

def quesSortByVotes(request,forum_id):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    userid = request.session['userid']
    role = request.session['role']

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()

    statement = """SELECT A.FORUM_ID,U.NAME,A.ANSWER_DESCRIPTION,A.ANS_TIME,A.ID,
                    (SELECT COUNT(*) FROM VOTE WHERE FORUM_ID = A.FORUM_ID AND FORUM_ANS_ID = A.ID) AS VOTES
                    FROM FORUM_ANS A,USERS U 
                    WHERE A.FORUM_ID = :i AND U.ID = A.PUBLISHER_ID ORDER BY VOTES DESC"""
    c.execute(statement,{'i':forum_id})
    ReplySet = c.fetchall()

    statement = """SELECT F.ID,F.TOPIC,F.QUESTION_DESCRIPTION,F.QUESTION_TIME,S.NAME
                    FROM FORUM_QUES F,USERS S
                    WHERE F.ID = :i AND S.ID = F.ST_ID"""
    
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
    statement = "SELECT PUBLISHER_ID FROM FORUM_ANS WHERE ID = :i"
    c.execute(statement,{'i':forum_ans_id})
    replier, = c.fetchall()
    if replier[0] == userid:
        return redirect('/forum/ques_details/'+str(forum_id))

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


def activity(request):
    if request.session.has_key('userid')== False:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    userid = request.session['userid']
    role= request.session['role']
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()

    statement = """SELECT ID,TOPIC, QUESTION_DESCRIPTION,QUESTION_TIME 
                FROM FORUM_QUES 
                WHERE ST_ID = :userid
                ORDER BY QUESTION_TIME DESC"""
    c.execute(statement,{'userid':userid})
    questions = c.fetchall()
    
    statement = """SELECT Q.ID, Q.TOPIC, Q.QUESTION_DESCRIPTION, A.ID, A.ANSWER_DESCRIPTION, A.ANS_TIME
                FROM FORUM_QUES Q, FORUM_ANS A
                WHERE A.PUBLISHER_ID = :userid AND A.FORUM_ID = Q.ID"""

    c.execute(statement,{'userid':userid})
    replies = c.fetchall()

    return render(request,'forum/activity.html',{'userid':userid,'role':role,'questions':questions,'replies':replies})

def ques_edit(request,forum_id):
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()
    statement = "UPDATE FORUM_QUES SET TOPIC = :t, QUESTION_DESCRIPTION = :q WHERE ID = :f"
    c.execute(statement,{'t':request.POST['title'],'q':request.POST['description'],'f':forum_id})
    connection.commit()
    c.close()
    connection.close()

    return redirect('/forum/activity')


def ans_edit(request,forum_ans_id):
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()
    statement = "UPDATE FORUM_ANS SET ANSWER_DESCRIPTION = :q WHERE ID = :f"
    c.execute(statement,{'q':request.POST['description'],'f':forum_ans_id})
    connection.commit()
    c.close()
    connection.close()

    return redirect('/forum/activity')

def ques_del(request,forum_id):
    print("QUESTION DELETE")
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()
    statement = "DELETE FORUM_QUES WHERE ID = :f"
    c.execute(statement,{'f':forum_id})
    connection.commit()
    c.close()
    connection.close()

    return redirect('/forum/activity')

def ans_del(request,forum_ans_id):
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    c = connection.cursor()
    statement = "DELETE FORUM_ANS WHERE ID = :f"
    c.execute(statement,{'f':forum_ans_id})
    connection.commit()
    c.close()
    connection.close()

    return redirect('/forum/activity')


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
        
        if text:
            c.execute(statement,(video_id,userid,text))
            #find related teacher id
            statement="""SELECT TC.TEACHER_ID
                        FROM CONTENTS C, TOPICS T, TAKE_COURSE TC 
                        WHERE C.ID = :video_id AND C.TOPIC_ID = T.ID AND T.COURSE_ID = TC.COURSE_ID"""
            c.execute(statement,{'video_id':video_id})
            teachers = c.fetchall()

            

            statement="""
                    INSERT INTO VIDEO_NOTIFICATIONS
                    VALUES(:0,:1,:2,SYSDATE,0)
                    """
            for teacher in teachers:
                if teacher[0] != userid:
                    c.execute(statement,(video_id,teacher[0],userid))
            

        
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
            #find related teacher id
            statement="""SELECT TC.TEACHER_ID
                        FROM CONTENTS C, TOPICS T, TAKE_COURSE TC 
                        WHERE C.ID = :video_id AND C.TOPIC_ID = T.ID AND T.COURSE_ID = TC.COURSE_ID"""
            c.execute(statement,{'video_id':video_id})
            teachers = c.fetchall()

            #find parent commenter_id
            statement="""SELECT COMMENTER_ID
                        FROM VIDEO_COMMENTS  
                        WHERE ID = :parent_id """
            c.execute(statement,{'parent_id':parent_id})
            parent_commenter ,= c.fetchone()

            statement="""
                    INSERT INTO VIDEO_NOTIFICATIONS
                    VALUES(:0,:1,:2,SYSDATE,0)
                    """
            for teacher in teachers:
                if teacher[0] != userid:
                    c.execute(statement,(video_id,teacher[0],userid))
            
            if  parent_commenter != userid:
                c.execute(statement,(video_id,parent_commenter,userid))

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