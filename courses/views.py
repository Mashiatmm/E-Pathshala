from django.shortcuts import render,redirect
from django.db import connection
import cx_Oracle

def add_course(request):#,t_id
    c = connection.cursor()

    if request.method=='POST':
        course_title=request.POST['course_title']
        course_class=request.POST['class']
        statement='INSERT INTO COURSES VALUES(1,%s,%s,%s)'
        c.execute(statement,(course_title,course_class,'0'))
        c.close()
        """c=connection.cursor()
        c.execute("select max(id) from COURSES where name = :course_title",{'course_title':request.POST['course_title']})
        course_id,=count.fetchone()
        statement='INSERT INTO TAKE_COURSE(TEACHER_ID,COURSE_ID) VALUES(%s,%s)'
        c.execute(statement,(t_id ,course_id))
        c.close()"""
        return render(request,'courses/add_course.html')
    else:
        return render(request,'courses/add_course.html')#,{'t_id':t_id}

