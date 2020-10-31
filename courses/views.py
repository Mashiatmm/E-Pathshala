from django.shortcuts import render,redirect
import cx_Oracle

#course title and class unique combo????

def add_course(request,id):

    if request.session.has_key('usermail') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})
    
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    usermail = request.session['usermail']
    statement = 'SELECT name FROM USERS WHERE email = : user_email'
    c.execute(statement,{'user_email':usermail})
    name, = c.fetchone()


    if request.method=='POST':

        course_title=request.POST['course_title']
        course_class=request.POST['class']

        try:
            statement='INSERT INTO COURSES VALUES(1,:0,:1,:2)'
            c.execute(statement,(course_title,course_class,'0'))

            statement = 'SELECT id FROM COURSES WHERE NAME = : title'
            c.execute(statement,{'title':course_title})
            c_id, = c.fetchone()
            statement = 'INSERT INTO TAKE_COURSE VALUES(:0,:1)'
            c.execute(statement,(c_id,id))
       
            c.close()
            connection.commit()
            connection.close()
       
            return render(request,'courses/add_course.html',{'usermail':usermail,'name': name,'t_id':id})

        except:
            c.close()
            connection.close()
            return render(request,'courses/add_course.html',{'usermail':usermail,'t_id':id,'error': 'Course name already exists'})
            
        

        
    else:
        c.close()
        connection.close()
        return render(request,'courses/add_course.html',{'usermail':usermail,'name': name,'t_id':id})

