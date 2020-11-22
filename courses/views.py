from django.shortcuts import render,redirect
import cx_Oracle



def add_course(request):
    userid = 0
    if request.session.has_key('userid'):
        userid = request.session['userid']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    userid = request.session['userid']


    if request.method=='POST':

        course_title=request.POST['course_title']
        course_class=request.POST['class']
        course_des = request.POST['course_description']

        try:
            statement="INSERT INTO COURSES VALUES(1,:0,:1,:2,sysdate,:3)"
            
            c.execute(statement,(course_title,course_class,'0',course_des))
            print('007')

            statement = "SELECT seq_course.currval FROM dual"
            c.execute(statement)
            c_id, = c.fetchone()
            
            statement = "INSERT INTO TAKE_COURSE VALUES(:0,:1)"
            c.execute(statement,(c_id,userid))
       
            c.close()
            connection.commit()
            connection.close()
       
            return redirect('/accounts/profile',{'userid':userid})
        
        except Exception as e:
            print(e)
            c.close()
            connection.close()
            return render(request,'courses/add_course.html',{'userid':userid,'role':'teacher','error': 'Course name already exists'})
            
        

        
    else:
        c.close()
        connection.close()
        return render(request,'courses/add_course.html',{'userid':userid,'role':'teacher'})


def del_course(request,course_id):
    userid = 0
    if request.session.has_key('userid'):
        userid = request.session['userid']

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()
    statement = """DELETE FROM QAS Q 
                WHERE Q.EXAM_ID = ANY(SELECT C.ID FROM CONTENTS C 
                WHERE C.TOPIC_ID = ANY(SELECT T.ID FROM TOPICS T WHERE T.COURSE_ID = :i))"""
    c.execute(statement,{'i':course_id})
    statement = "DELETE FROM COURSES WHERE ID = :i"
    c.execute(statement,{'i':course_id})
    c.close()
    connection.commit()
    connection.close()
    
    return redirect('/accounts/profile',{'userid':userid})

def edit_course(request,course_id):
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    statement = """UPDATE COURSES
                   SET NAME = :N,CLASS = :C,COURSE_DESCRIPTION = :D
                   WHERE ID = :i"""
    c.execute(statement,{'N':request.POST['title'],'C':request.POST['class'],'D':request.POST['Description'],'i':course_id})
    
    connection.commit()
    c.close()
    connection.close()
    return redirect('/courses/course_contents/teacher/'+str(course_id)+'/')


def course_contents(request,course_id):
    userid = 0
    if request.session.has_key('userid'):
        userid = request.session['userid']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    
    error = ""

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()
    print(request.method)
    if request.method == 'POST':
        
        try:   
            statement="Insert into TOPICS(COURSE_ID,TOPIC_TITLE,TOPIC_DESCRIPTION) VALUES(:0,:1,:2)"
            c.execute(statement,(course_id,request.POST['topic'],request.POST['topic_description']))

        
        except Exception as e:
            error = "Topic name exists or empty"
          
    

    statement = "select name,class,course_description from Courses where id = :id "
    c.execute(statement,{'id':course_id})
    courseinfo, = c.fetchall()
    #WRITE FUNCTION TO RETURN CONTENT NUMBERS
    statement = """SELECT T.ID,T.TOPIC_TITLE,T.TOPIC_DESCRIPTION
                    FROM TOPICS T
                    WHERE T.COURSE_ID = :course_id"""
    c.execute(statement,{'course_id':course_id})
    topics = c.fetchall()
    print(topics)
    c.close()
    connection.commit()
    connection.close()
    if error == "":
        return render(request,'courses/course_contents.html',{'course_id':course_id,'courseinfo':courseinfo,'topics':topics,'userid':userid,'role':'teacher'})
    else:
        return render(request,'courses/course_contents.html',{'course_id':course_id,'courseinfo':courseinfo,'topics':topics,'userid':userid,'error':error,'role':'teacher'})


def del_topic(request,course_id,topic_id):
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()
    statement = "DELETE FROM QAS Q WHERE Q.EXAM_ID = ANY(SELECT C.ID FROM CONTENTS C WHERE C.TOPIC_ID = :i)"
    c.execute(statement,{'i':topic_id})
    statement = "DELETE FROM TOPICS WHERE ID = :i"
    c.execute(statement,{'i':topic_id})
    c.close()
    connection.commit()
    connection.close()
    
    return redirect('/courses/course_contents/teacher/'+str(course_id)+'/')

def topic_details(request,topic_id):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    userid = request.session['userid']
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    statement = """SELECT C.SL_NO,C.TITLE,C.DESCRIPTION,C.CONTENT_TYPE,E.TOTAL_MARKS,V.LINK,C.DURATION,C.ID
                    FROM CONTENTS C, EXAMS E, VIDEOS V
                    WHERE C.TOPIC_ID = :t AND C.ID = E.ID(+) AND C.ID = V.ID(+)
                    ORDER BY C.SL_NO"""
    c.execute(statement,{'t':topic_id})
    contents = c.fetchall()

    statement = """SELECT T.ID,T.TOPIC_TITLE,T.TOPIC_DESCRIPTION,C.NAME,C.CLASS,C.ID 
                FROM TOPICS T,COURSES C
                WHERE T.COURSE_ID = C.ID AND T.ID = :t"""
    c.execute(statement,{'t':topic_id})
    topic_details = c.fetchone()

    if request.session.has_key('error'):
        error = request.session['error']
        print(error)
        del request.session['error']
        return render(request,'courses/topic.html',{'contents':contents,'topic_details':topic_details,'userid':userid,'role':'teacher','error':error})
    return render(request,'courses/topic.html',{'contents':contents,'topic_details':topic_details,'userid':userid,'role':'teacher'})


def update_topic(request,topic_id):
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    statement = """UPDATE TOPICS
                   SET TOPIC_TITLE = :T,TOPIC_DESCRIPTION = :D
                   WHERE ID = :i"""
    c.execute(statement,{'T':request.POST['title'],'D':request.POST['Description'],'i':topic_id})
    
    connection.commit()
    c.close()
    connection.close()
    return redirect('/courses/topic_details/'+str(topic_id)+'/')


def modify_content(request,topic_id,content_type,content_id):
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()
    statement = """UPDATE CONTENTS
                    SET TITLE = :t, DESCRIPTION = :d
                    WHERE ID = :i""" 
    c.execute(statement,{'i':content_id,'t':request.POST['title'],'d':request.POST['description']})
    connection.commit()
    if content_type == 'exam':
        c.close()
        connection.close()
        return redirect('/courses/add_ques/'+str(content_id)+'/')
    else:
        statement = """UPDATE VIDEOS
                    SET LINK = :l 
                    WHERE ID = :i""" 
        c.execute(statement,{'i':content_id,'l':request.POST['videourl']})
        connection.commit()
        c.close()
        connection.close()
        return redirect('/courses/topic_details/'+str(topic_id)+'/')

def del_content(request,topic_id,content_id):
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()
    statement = "DELETE FROM QAS WHERE EXAM_ID = :i"
    c.execute(statement,{'i':content_id})
    statement = "DELETE FROM CONTENTS WHERE ID = :i"
    c.execute(statement,{'i':content_id})
    c.close()
    connection.commit()
    connection.close()
    return redirect('/courses/topic_details/'+str(topic_id)+'/')


def add_content(request,course_id,topic_id):#add video
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    if request.method == 'POST':
        
        try:
            statement = """INSERT INTO CONTENTS(TOPIC_ID,ID,SL_NO,TITLE,DESCRIPTION,CONTENT_TYPE)
                         VALUES(:0,0,0,:1,:2,'video')"""
            c.execute(statement,(topic_id,request.POST['videotitle'],request.POST['Description']))
            statement = "SELECT seq_content.currval FROM dual"
            c.execute(statement)
            content_id, = c.fetchone()
            print(content_id)
            statement = "INSERT INTO VIDEOS VALUES(:0,:1)"
            c.execute(statement,(content_id,request.POST['videourl']))
        except Exception as e:
            error = "Same video/ title exists "
            print(e)
            request.session['error'] = error
            return redirect('/courses/topic_details/'+str(topic_id)+'/')



    c.close()
    connection.commit()
    connection.close()
    
    return redirect('/courses/topic_details/'+str(topic_id)+'/')

def add_exams(request,course_id,topic_id):
    
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    userid = request.session['userid']
    
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    if request.method == 'POST':
        try:
                statement = """INSERT INTO CONTENTS(TOPIC_ID,ID,SL_NO,TITLE,DESCRIPTION,CONTENT_TYPE)
                                VALUES(:0,0,1,:1,:2,'exam')"""
                c.execute(statement,(topic_id,request.POST['title'],request.POST['details']))
                connection.commit()
                
                statement = "SELECT seq_content.currval FROM dual"
                c.execute(statement)
                content_id, = c.fetchone()
                print(content_id)
                statement = "INSERT INTO EXAMS VALUES(:0,:1)"
                c.execute(statement,(content_id,0))
            
                examinfo = [request.POST['title'],request.POST['details'],content_id]
            
                c.close()
                connection.commit()   
                connection.close()

                return render(request,'courses/add_exam.html',{'userid':userid,'course_id':course_id,'topic_id':topic_id,'examinfo':examinfo,'role':'teacher'})
            
        except:
                c.close()
                connection.close()
                error = "Same Title exists"
                return render(request,'courses/add_exam.html',{'userid':userid,'course_id':course_id,'topic_id':topic_id,'error':error,'role':'teacher'})
            
            
            
    return render(request,'courses/add_exam.html',{'userid':userid,'course_id':course_id,'topic_id':topic_id,'role':'teacher'})

def add_ques(request,exam_id):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    userid = request.session['userid']
    print(request.method)
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()
    statement = "SELECT TITLE,DESCRIPTION,TOPIC_ID FROM CONTENTS WHERE ID = :i"
    c.execute(statement,{'i':exam_id})
    info, = c.fetchall()
    
    examinfo = [info[0],info[1],exam_id]
    topic_id = info[2]

    if request.method == 'POST':
        right_option = request.POST.get('Radios')
        statement = "INSERT INTO QAS(EXAM_ID,QUESTION_DESCRIPTION,OPTION1,OPTION2,OPTION3,OPTION4) VALUES(:0,:1,:2,:3,:4,:5)"
        c.execute(statement,(exam_id,request.POST['questiontitle'],request.POST['option1'],request.POST['option2'],request.POST['option3'],request.POST['option4']))
        statement = "SELECT seq_ques.currval FROM dual"
        c.execute(statement)
        ques_id, = c.fetchone()
        statement = "INSERT INTO QA_ANS(ID,RIGHT_OPTION) VALUES(:0,:1)"
        c.execute(statement,(ques_id,right_option))
        #Handle Multiple values
        connection.commit()
        return redirect('/courses/add_ques/'+str(exam_id)+'/')

    statement = """SELECT Q.QUESTION_DESCRIPTION,Q.OPTION1,Q.OPTION2,Q.OPTION3,Q.OPTION4,A.RIGHT_OPTION,Q.ID
                    FROM QAS Q, QA_ANS A
                    WHERE Q.EXAM_ID = :e AND A.ID = Q.ID
                    ORDER BY Q.ID"""
    c.execute(statement,{'e':exam_id})
    ques_list = c.fetchall()     
    c.close()
    connection.close()

    return render(request,'courses/add_exam.html',{'userid':userid,'topic_id':topic_id,'examinfo':examinfo,'role':'teacher','ques_list':ques_list})


def del_ques(request,exam_id,ques_id):
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    statement = "DELETE FROM QAS WHERE ID = :i"
    c.execute(statement,{'i':ques_id})
    c.close()
    connection.commit()
    connection.close()
    return redirect('/courses/add_ques/'+str(exam_id)+'/')

def edit_ques(request,exam_id,ques_id):
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    statement = """UPDATE QAS
                   SET QUESTION_DESCRIPTION = :d,OPTION1 = :o1,OPTION2 = :o2,OPTION3 = :o3,OPTION4 = :o4 
                   WHERE ID = :i"""
    c.execute(statement,{'d':request.POST['questitle'],'o1':request.POST['option1'],'o2':request.POST['option2'],'o3':request.POST['option3'],'o4':request.POST['option4'],'i':ques_id})
    
    statement = """UPDATE QA_ANS
                   SET RIGHT_OPTION = :r 
                   WHERE ID = :i"""
    c.execute(statement,{'i':ques_id,'r':request.POST.get('Radios')})
    connection.commit()
    c.close()
    connection.close()
    return redirect('/courses/add_ques/'+str(exam_id)+'/')
    


def enroll_course(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()
    if request.method == 'POST':
        statement = "insert into enroll values(:0,:1,0,sysdate)"
        c.execute(statement,(userid,request.POST['course_id']))

    connection.commit()
    statement = """ select id,name,total_marks 
                    from courses c 
                    where c.class = (select class from students where id = :st_id)
                            and c.id not in(select course_id from enroll where st_id = :st_id )"""
    c.execute(statement,{'st_id':userid})
    available_courses = c.fetchall()
    print(available_courses)
    c.close()
    connection.close()
    #,{'userid':userid,'available_courses':available_courses}
    return render(request,'courses/enroll_course.html',{'userid':userid,'available_courses':available_courses,'role':'student'}) 


def all_courses_student(request,id):
    if request.session.has_key('userid'):
        userid = request.session['userid']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()
    statement="select id,name from courses where id in (select course_id from enroll where st_id = :s_id) "
    c.execute(statement,{'s_id':userid})
    courses=c.fetchall()
    c.close()
    connection.close()
    
    return render(request,'courses/all_courses_student.html',{'courses':courses,'userid':userid,'role':'student'})

def course_topics_student(request,course_id):
    if request.session.has_key('userid'):
        userid = request.session['userid']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()  

    statement= "SELECT ID,NAME FROM COURSES WHERE ID = :course_id"
    c.execute(statement,{'course_id':course_id})
    course = c.fetchone()

    statement = "SELECT * FROM ENROLL WHERE ST_ID = :userid AND COURSE_ID = :course_id"
    c.execute(statement,{'userid':userid,'course_id':course_id})
    enroll_record = c.fetchone()   
    

    statement= "SELECT ID,TOPIC_TITLE,TOPIC_DESCRIPTION FROM TOPICS WHERE COURSE_ID = :course_id"
    c.execute(statement,{'course_id':course_id})
    topics= c.fetchall()
    c.close()
    connection.close() 

    return render(request,'courses/course_topics_student.html',{'userid':userid,'topics': topics,'course':course,'enroll_record':enroll_record})



def course_contents_student(request,topic_id):
    if request.session.has_key('userid'):
        userid = request.session['userid']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor() 

    statement = "SELECT T.COURSE_ID,C.NAME,T.TOPIC_TITLE FROM TOPICS T,COURSES C WHERE T.COURSE_ID = C.ID AND T.ID = :topic_id"
    c.execute(statement,{'topic_id':topic_id})
    courseNtopic = c.fetchone()#stores info about the topic and course

    statement = "SELECT * FROM ENROLL WHERE ST_ID = :userid AND COURSE_ID = :course_id"
    c.execute(statement,{'userid':userid,'course_id':courseNtopic[0]})
    enroll_record = c.fetchone()




    statement= "SELECT ID,TITLE,DESCRIPTION,CONTENT_TYPE,DURATION FROM CONTENTS WHERE TOPIC_ID = :topic_id order by sl_no"
    c.execute(statement,{'topic_id':topic_id})
    contents= c.fetchall() 
    c.close()
    connection.close() 
    return render(request,'courses/course_contents_student.html',{'userid':userid,'contents':contents,'courseNtopic':courseNtopic,'enroll_record':enroll_record})

def show_video(request,content_id):
    if request.session.has_key('userid'):
        userid = request.session['userid']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor() 

    statement="SELECT CRS.NAME,T.TOPIC_TITLE,C.TITLE,C.DESCRIPTION,V.LINK FROM VIDEOS V,CONTENTS C,TOPICS T, COURSES CRS WHERE V.ID = C.ID AND C.TOPIC_ID=T.ID AND T.COURSE_ID = CRS.ID AND V.ID= :content_id"
    c.execute(statement,{'content_id':content_id})
    video = c.fetchone()
    c.close()
    connection.close() 
    
    return render(request,'contents/show_video.html',{'userid':userid,'video': video,'content_id':content_id})


def give_exam(request,content_id):
    if request.session.has_key('userid'):
        userid = request.session['userid']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor() 

    if request.method == 'POST':
        statement="SELECT Q.ID,A.RIGHT_OPTION FROM QAS Q,QA_ANS A WHERE Q.EXAM_ID = :content_id AND A.ID=Q.ID ORDER BY Q.ID"
        c.execute(statement,{'content_id':content_id})
        questions= c.fetchall()
        marks=0

        for question in questions:
            if request.POST.get('q'+str(question[0])) == question[1]:
                marks=marks+1
        statement="INSERT INTO COMPLETED_CONTENT VALUES(:0,:1,:2)"
        c.execute(statement,(content_id,userid,marks))
        connection.commit()



        statement="SELECT T.ID FROM CONTENTS C,TOPICS T WHERE C.TOPIC_ID = T.ID AND C.ID = :content_id"
        c.execute(statement,{'content_id':content_id})
        topic_id,= c.fetchone()
            
        c.close()
        connection.close() 
        return redirect('/courses/course_contents/student/'+str(topic_id))
        
    statement="SELECT CONTENT_ID FROM COMPLETED_CONTENT WHERE CONTENT_ID = :content_id AND ST_ID = :userid"
    c.execute(statement,{'content_id':content_id,'userid':userid})
    entry = c.fetchone()

    statement="SELECT C.TOPIC_ID,C.TITLE,E.TOTAL_MARKS FROM EXAMS E,CONTENTS C WHERE E.ID = C.ID AND E.ID= :content_id"
    c.execute(statement,{'content_id':content_id})
    exam = c.fetchone()

    statement="SELECT ID,QUESTION_DESCRIPTION,OPTION1,OPTION2,OPTION3,OPTION4 FROM QAS WHERE EXAM_ID = :content_id ORDER BY ID"
    c.execute(statement,{'content_id':content_id})
    questions= c.fetchall()
    

    
 

    if entry == None:
        c.close()
        connection.close() 
        return render(request,'contents/give_exam.html',{'userid':userid,'content_id':content_id,'exam': exam,'questions':questions})

    c.close()
    connection.close()
    return render(request,'contents/give_exam.html',{'userid':userid,'content_id':content_id,'exam': exam,'questions':questions,'error':'You have already given the exam ! '})
    



