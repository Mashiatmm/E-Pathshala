from django.shortcuts import render,redirect
import cx_Oracle

#course title and class unique combo????

def all_courses(request,id):
    if request.session.has_key('userid'):
        userid = request.session['userid']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})

            
    
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()
    statement="select id,name,class from courses where id in (select course_id from take_course where teacher_id =: t_id) "
    c.execute(statement,{'t_id':id})
    courses=c.fetchall()
    print(len(courses))
    c.close()
    connection.close()
    
    return render(request,'courses/all_courses.html',{'t_id':id,'courses':courses,'userid':userid})


def add_course(request,id):

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

            #statement = 'SELECT id FROM COURSES WHERE NAME = : title and class = :c'
            #c.execute(statement,{'title':course_title,'c': course_class})
            statement = "SELECT seq_course.currval FROM dual"
            c.execute(statement)
            c_id, = c.fetchone()
            
            statement = "INSERT INTO TAKE_COURSE VALUES(:0,:1)"
            c.execute(statement,(c_id,id))

            statement="select id,name,class from courses where id in (select course_id from take_course where teacher_id =: t_id) "
            c.execute(statement,{'t_id':id})
            courses=c.fetchall()
       
            c.close()
            connection.commit()
            connection.close()
       
            return render(request,'courses/all_courses.html',{'t_id':id,'courses':courses,'userid':userid})
        
        except:
            c.close()
            connection.close()
            return render(request,'courses/add_course.html',{'userid':userid,'t_id':id,'error': 'Course name already exists'})
            
        

        
    else:
        c.close()
        connection.close()
        return render(request,'courses/add_course.html',{'userid':userid,'t_id':id})


def course_contents(request,course_id):
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
            error = "Topic name for the same course exists"
            
    

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
        return render(request,'courses/course_contents.html',{'course_id':course_id,'courseinfo':courseinfo,'topics':topics,'userid':userid})
    else:
        return render(request,'courses/course_contents.html',{'course_id':course_id,'courseinfo':courseinfo,'topics':topics,'userid':userid,'error':error})

def add_exams(request,course_id,topic_id):
    print(request.POST)
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    userid = request.session.has_key('userid')
    
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

                return render(request,'courses/add_exam.html',{'userid':userid,'course_id':course_id,'topic_id':topic_id,'examinfo':examinfo})
            
        except:
                c.close()
                connection.close()
                error = "Same Title exists"
                return render(request,'courses/add_exam.html',{'userid':userid,'course_id':course_id,'topic_id':topic_id,'error':error})
            
            
            
    return render(request,'courses/add_exam.html',{'userid':userid,'course_id':course_id,'topic_id':topic_id})

def add_ques(request,exam_id):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    userid = request.session.has_key('userid')
    
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

        return render(request,'courses/add_exam.html',{'userid':userid,'examinfo':examinfo})


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
    
      






'''
<form class="form-settings" action="{% url 'courses:add_content' course_id %}" method="POST" >
                {% csrf_token %}
                    <button class="btn btn-lg btn-outline-primary btn-block mb-5" type="submit">Add Video</button>
                </form> 



                <button class="btn btn-lg btn-outline-primary btn-block mb-5">Confirm 1</button>

                <a class="btn btn-primary" href="{% url 'courses:add_content' course_id %}" role="button">Confirm</a>
'''