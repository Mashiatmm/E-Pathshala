from django.shortcuts import render,redirect
import cx_Oracle

#course title and class unique combo????

def all_courses(request,id):
    if request.session.has_key('usermail'):
        usermail = request.session['usermail']
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
    
    return render(request,'courses/all_courses.html',{'t_id':id,'courses':courses,'usermail':usermail})


def add_course(request,id):

    if request.session.has_key('usermail'):
        usermail = request.session['usermail']
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    usermail = request.session['usermail']
    statement = "SELECT name FROM USERS WHERE email = : user_email"
    c.execute(statement,{'user_email':usermail})
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
       
            return render(request,'courses/all_courses.html',{'t_id':id,'courses':courses,'usermail':usermail})

        except:
            c.close()
            connection.close()
            return render(request,'courses/add_course.html',{'usermail':usermail,'t_id':id,'error': 'Course name already exists'})
            
        

        
    else:
        c.close()
        connection.close()
        return render(request,'courses/add_course.html',{'usermail':usermail,'t_id':id})


def course_contents(request,course_id):
    if request.session.has_key('usermail'):
        usermail = request.session['usermail']
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

    statement = """SELECT T.ID,T.TOPIC_TITLE,C.CONTENT_TYPE, C.TITLE, C.DESCRIPTION,C.ID
                    FROM TOPICS T, CONTENTS C
                    WHERE T.ID = C.TOPIC_ID(+) AND T.COURSE_ID = :course_id
                    ORDER BY NVL(C.SL_NO,0)"""
    c.execute(statement,{'course_id':course_id})
    topics = c.fetchall()
    print(topics)
    c.close()
    connection.commit()
    connection.close()
    if error == "":
        return render(request,'courses/course_contents.html',{'course_id':course_id,'courseinfo':courseinfo,'topics':topics,'usermail':usermail})
    else:
        return render(request,'courses/course_contents.html',{'course_id':course_id,'courseinfo':courseinfo,'topics':topics,'usermail':usermail,'error':error})


def add_content(request,course_id,topic_id):
    if request.session.has_key('usermail') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    usermail = request.session.has_key('usermail')
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    if request.method == 'POST':
        statement = """INSERT INTO CONTENTS(TOPIC_ID,ID,SL_NO,TITLE,DESCRIPTION,CONTENT_TYPE)
                     VALUES(:0,0,1,:1,:2,'video')"""
        c.execute(statement,(topic_id,request.POST['videotitle'],request.POST['Description']))
        statement = "SELECT seq_content.currval FROM dual"
        c.execute(statement)
        content_id, = c.fetchone()
        statement = "INSERT INTO VIDEOS VALUES(:0,:1)"
        c.execute(statement,(content_id,request.POST['videourl']))

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