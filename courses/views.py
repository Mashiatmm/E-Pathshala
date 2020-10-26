from django.shortcuts import render,redirect
from django.db import connection
import cx_Oracle

def add_course(request):
    c = connection.cursor()

    if request.method=='POST':
        course_title=request.POST['course_title']
        course_class=request.POST['class']
        statement='INSERT INTO COURSES VALUES(1,%s,%s,%s)'
        c.execute(statement,(course_title,course_class,'0'))
        c.close()
        return render(request,'courses/add_course.html')
    else:
        return render(request,'courses/add_course.html')

