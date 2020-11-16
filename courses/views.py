from django.shortcuts import render,redirect
import cx_Oracle


def all_courses(request):
    userid = 0
    if request.session.has_key('userid'):
        userid = request.session['userid']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In','role':'teacher'})

            
    
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()
    statement="select id,name,class from courses where id in (select course_id from take_course where teacher_id =: t_id) "
    c.execute(statement,{'t_id':userid})
    courses=c.fetchall()
    print(len(courses))
    c.close()
    connection.close()
    
    return render(request,'courses/all_courses.html',{'courses':courses,'userid':userid,'role':'teacher'})


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
    statement = "SELECT name FROM USERS WHERE id = : user_id"
    c.execute(statement,{'user_id':userid})
    name, = c.fetchone()


    if request.method=='POST':

        course_title=request.POST['course_title']
        course_class=request.POST['class']

        try:
            statement="INSERT INTO COURSES VALUES(1,:0,:1,:2,sysdate)"
            
            c.execute(statement,(course_title,course_class,'0'))
            print('007')

            statement = "SELECT seq_course.currval FROM dual"
            c.execute(statement)
            c_id, = c.fetchone()
            
            statement = "INSERT INTO TAKE_COURSE VALUES(:0,:1)"
            c.execute(statement,(c_id,userid))

            statement="select id,name,class from courses where id in (select course_id from take_course where teacher_id =: t_id) "
            c.execute(statement,{'t_id':userid})
            courses=c.fetchall()
       
            c.close()
            connection.commit()
            connection.close()
       
            return render(request,'courses/all_courses.html',{'courses':courses,'userid':userid,'role':'teacher'})
        
        except:
            c.close()
            connection.close()
            return render(request,'courses/add_course.html',{'userid':userid,'role':'teacher','error': 'Course name already exists'})
            
        

        
    else:
        c.close()
        connection.close()
        return render(request,'courses/add_course.html',{'userid':userid,'role':'teacher'})


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

    if request.method == 'POST':
        
        try:   
            statement="Insert into TOPICS(COURSE_ID,TOPIC_TITLE) VALUES(:0,:1)"
            c.execute(statement,(course_id,request.POST['topic']))

        
        except Exception as e:
            error = "Topic name exists or empty"
          
    

    statement = "select name,class from Courses where id = :id "
    c.execute(statement,{'id':course_id})
    courseinfo, = c.fetchall()
   
    statement = """SELECT T.ID,T.TOPIC_TITLE,COUNT(C.ID)
                    FROM TOPICS T, CONTENTS C
                    WHERE T.COURSE_ID = :course_id AND C.TOPIC_ID(+) = T.ID
                    GROUP BY(T.ID,T.TOPIC_TITLE)"""
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
    
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()
    statement = "SELECT TITLE,DESCRIPTION FROM CONTENTS WHERE ID = :i"
    c.execute(statement,{'i':exam_id})
    info, = c.fetchall()
    print(info)
    examinfo = [info[0],info[1],exam_id]

    if request.method == 'POST':
        answer_options = [request.POST['option1'],request.POST['option2'],request.POST['option3'],request.POST['option4']]
        right_option = request.POST[request.POST.get('Radios')]
        print(right_option)
        statement = "INSERT INTO QAS(EXAM_ID,QUESTION_DESCRIPTION) VALUES(:0,:1)"
        c.execute(statement,(exam_id,request.POST['questiontitle']))
        statement = "SELECT seq_ques.currval FROM dual"
        c.execute(statement)
        ques_id, = c.fetchone()
        right_opt_id = 0
        statement = "INSERT INTO QA_ANS(QA_ID,ANS_OPTION) VALUES(:0,:1)"
        for i in range(len(answer_options)):
            c.execute(statement,(ques_id,answer_options[i]))
            if right_option == answer_options[i]:
                right_opt_id = c.execute("SELECT seq_ans.currval FROM dual")
                right_opt_id, = c.fetchone()
        

        statement = "UPDATE QAS SET RIGHT_OPTION = :r WHERE ID = :i"
        c.execute(statement,{'r':right_opt_id,'i':ques_id})

        c.close()
        connection.commit()
        connection.close()

        return render(request,'courses/add_exam.html',{'userid':userid,'examinfo':examinfo,'role':'teacher'})


def add_content(request,course_id,topic_id):
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    if request.method == 'POST':
        
        try:
            statement = """INSERT INTO CONTENTS(TOPIC_ID,ID,SL_NO,TITLE,DESCRIPTION,CONTENT_TYPE)
                         VALUES(:0,0,1,:1,:2,'video')"""
            c.execute(statement,(topic_id,request.POST['videotitle'],request.POST['Description']))
            statement = "SELECT seq_content.currval FROM dual"
            c.execute(statement)
            content_id, = c.fetchone()
            print(content_id)
            statement = "INSERT INTO VIDEOS VALUES(:0,:1)"
            c.execute(statement,(content_id,request.POST['videourl']))
        except:
            error = "Same video/ title exists "
            print(error)
            #show message



    c.close()
    connection.commit()
    connection.close()
    
    return redirect('/courses/course_contents/'+str(course_id)+'/')
    
      
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