from django.shortcuts import render,redirect
import cx_Oracle

#course title and class unique combo????

def all_courses(request,id):
    if request.session.has_key('usermail') == False:
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
    
    return render(request,'courses/all_courses.html',{'t_id':id,'courses':courses})


def add_course(request,id):

    if request.session.has_key('usermail') == False:
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
       
            c.close()
            connection.commit()
            connection.close()
       
            return render(request,'courses/all_courses.html',{'t_id':id})

        except:
            c.close()
            connection.close()
            return render(request,'courses/add_course.html',{'usermail':usermail,'t_id':id,'error': 'Course name already exists'})
            
        

        
    else:
        c.close()
        connection.close()
        return render(request,'courses/add_course.html',{'usermail':usermail,'t_id':id})


def course_contents(request,course_id):
    if request.session.has_key('usermail') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()
    statement="select C.id,T.topic_title,C.sl_no,C.title,C.description,C.content_type,C.duration  from contents C,topics T where T.course_id =: course_id and C.topic_id = T.id"
    c.execute(statement,{'course_id':course_id})
    contents=c.fetchall()
    return render(request,'courses/course_contents.html',{'course_id':course_id,'contents':contents})

def add_content(request,course_id):
    if request.session.has_key('usermail') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    if request.method=='POST':
        render(request,'courses/course_contents.html',{'course_id':course_id,'contents':contents})

    else:
        c.close()
        connection.close()
        render(request,'courses/add_content.html',{'course_id':course_id})


