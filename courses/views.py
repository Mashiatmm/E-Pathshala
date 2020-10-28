from django.shortcuts import render,redirect
from django.db import connection
import cx_Oracle

def add_course(request,id):#,t_id
    c = connection.cursor()

    if request.method=='POST':
        course_title=request.POST['course_title']
        course_class=request.POST['class']
        statement='INSERT INTO COURSES VALUES(1,%s,%s,%s)'
        c.execute(statement,(course_title,course_class,'0'))

        statement = 'SELECT id FROM COURSES WHERE NAME = : title'
        c.execute(statement,{'title':course_title})
        c_id, = c.fetchone()
        print(c_id)
        

        statement = 'INSERT INTO TAKE_COURSE VALUES(%s,%s)'
        c.execute(statement,(c_id,id))
       
        c.close()
       
        return render(request,'courses/add_course.html',{'t_id':id})
    else:
        return render(request,'courses/add_course.html',{'t_id':id})

