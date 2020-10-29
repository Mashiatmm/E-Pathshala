from django.shortcuts import render,redirect
import cx_Oracle

def add_course(request,id):

    if request.session.has_key('usermail') == False:
            return render(request,'accounts/profile.html',{'error': 'Not Logged In'})

    if request.method=='POST':
        dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
        connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
        c = connection.cursor()

        course_title=request.POST['course_title']
        course_class=request.POST['class']
        statement='INSERT INTO COURSES VALUES(1,:0,:1,:2)'
        c.execute(statement,(course_title,course_class,'0'))

        statement = 'SELECT id FROM COURSES WHERE NAME = : title'
        c.execute(statement,{'title':course_title})
        c_id, = c.fetchone()
        

        statement = 'INSERT INTO TAKE_COURSE VALUES(:0,:1)'
        c.execute(statement,(c_id,id))
       
        c.close()
        connection.close()
       
        return render(request,'courses/add_course.html',{'t_id':id,'role': 'teacher'})
    else:
        return render(request,'courses/add_course.html',{'t_id':id,'role': 'teacher'})

