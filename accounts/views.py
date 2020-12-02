from django.shortcuts import render,redirect
import cx_Oracle
from passlib.hash import argon2


#Mashiat Virtual Env - 'myvenv'
#Teacher Specialty Multivalued?? Checkbox??

def home(request):
    '''
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    
    c = connection.cursor()
    statement = 'select id,password from USERS'
    c.execute(statement)
    passwords = c.fetchall()
  
    
    for i in range(len(passwords)):
        hash_pass = argon2.hash(passwords[i][1])
       
        statement = 'update USERS set password = :p where id = :i '
        c.execute(statement, {'p': hash_pass, 'i': passwords[i][0]})
    
    c.close()
    connection.commit()
    connection.close()
    '''
    '''dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    
    c = connection.cursor()
    statement = "SELECT ID,NAME,CLASS FROM COURSES " '''
       
    home=1
    if request.session.has_key('userid'):
        userid = request.session['userid']
        role= request.session['role']
        return render(request,'accounts/home.html',{'userid':userid,'role':role,'home':home})

    return render(request,'accounts/home.html',{'home':home})


def signup(request,role):

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    
    c = connection.cursor()

    if request.method=='POST':
        
    
        if request.POST['password1']==request.POST['password2']:

            try:
                    
                hash_pass = argon2.hash(request.POST['password2'])
                print(request.POST['username'], request.POST['email'],hash_pass,role)
                statement = 'insert into USERS(name,email, password,role,sign_up_time) values (:0,:1,:2,:3,sysdate)'
                c.execute(statement, (request.POST['username'], request.POST['email'],hash_pass,role))
                
                #c.execute("select id from USERS where email = :usermail",{'usermail':request.POST['email']})
                c.execute("select seq_user.currval from dual")
                val,=c.fetchone()

                
                if role== 'student':
                    statement='insert into STUDENTS(id,class) values (:0,:1)'
                    c.execute(statement,(val,request.POST['grade']))
                    
                else:
                    statement='insert into TEACHERS(id,specialty) values (:0,:1)'
                    c.execute(statement,(val,request.POST['specialty']))
                
                c.close()

                connection.commit()
                connection.close()
                if request.session.has_key('userid'):
                    del request.session['userid']
                    del request.session['role']
                request.session['userid'] = val
                request.session['role'] = role
                return redirect('/accounts/profile',{'userid':val})
                #return render(request,'accounts/profile.html',{'id':val,'role':role,'name':request.POST['username'],'email':request.POST['email'],'password':request.POST['password2']})
            except Exception as E: 
                print(E) 
                c.close()  
                connection.close()
                return render(request,'accounts/signup.html',{'role':role,'error':"Email already taken!"})
        
        else:
            c.close()
            connection.close()
            return render(request,'accounts/signup.html',{'role':role,'error':"Passwords didn't match!"})
    
    else:
        if role == 'student':
            c.close()
            connection.close()
            return render(request,'accounts/signup.html',{'role':role})
        else:
            statement='select distinct specialty from TEACHERS'
            c.execute(statement)
            all_spec=c.fetchall()
            all_specialties=[]
            for spec in all_spec:
                all_specialties.append(spec[0])

            c.close()

            connection.commit()
            connection.close()
            return render(request,'accounts/signup.html',{
                'role':role,
                'all_specialties':all_specialties
            })

        


def login(request):
    if request.method=='POST':

        dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
        connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
        
        c = connection.cursor()
        email= request.POST['email_or_name']
        statement= 'select email from USERS where email=:mail'
        c.execute(statement,{'mail':email})
        user_exists=c.fetchall()

        if user_exists == [] :
            c.close()
            connection.close()
            return render(request,'accounts/login.html',{'error':"Mail ID Does Not Exist!!!"})

        else:
            statement="select password,role,id from USERS where email=:mail"
            c.execute(statement,{'mail':email})
            info= c.fetchone()

            if(argon2.verify(request.POST['password'],info[0])):
                c.close()

                if request.session.has_key('userid'):
                    del request.session['userid']
                    del request.session['role']

                request.session['userid'] = info[2]
                request.session['role'] = info[1]
                
                connection.close()
                return redirect('/accounts/profile',{'userid':info[2]})
                #return redirect('/accounts/'+info[1]+'/'+str(info[2]))

            else:
                c.close()
                connection.close()
                return render(request,'accounts/login.html',{'error':"Incorrect Password!!"})
                
    
    else:
        try:
            del request.session['userid']
        except:
            pass
        return render(request,'accounts/login.html')



def profile(request):

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    if request.session.has_key('userid'):
        userid = request.session['userid']

        c = connection.cursor()

        statement = "select role from USERS where id=:id"
        c.execute(statement,{'id':userid})  
        role,= c.fetchone()
        if role=="student":
            statement="""Select U.NAME,S.CLASS 
                        FROM USERS U, STUDENTS S 
                        WHERE S.ID=U.ID AND U.ID=:user_id"""
            c.execute(statement,{'user_id': userid})
            user,=c.fetchall()

            statement="select id,name,class,course_description from courses where id in (select course_id from enroll where st_id = :userid) "
            c.execute(statement,{'userid':userid})
            courses=c.fetchall()


            
        else:
            statement="""Select U.NAME,T.Specialty 
                        FROM USERS U, TEACHERS T
                        WHERE T.ID=U.ID AND U.ID=:user_id"""
            c.execute(statement,{'user_id': userid})
            user,=c.fetchall()
            statement="""select c.id,c.name,c.class
                        from courses c
                        where c.id in (select course_id from take_course where teacher_id =:userid)"""
            c.execute(statement,{'userid':userid})
            courses=c.fetchall()

        c.close()
        connection.close()  
        if request.session.has_key('error'):
            error = request.session['error']
            print(error)
            del request.session['error']
            return render(request,'accounts/profile.html',{'userid':userid,'role':role,'name':user[0],'courses':courses,'error':error})
        return render(request,'accounts/profile.html',{'userid':userid,'role':role,'name':user[0],'courses':courses})    

        
    
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})


def settings(request):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    userid = request.session['userid']
    statement = 'SELECT role,name,password,email FROM USERS WHERE id = : user_id'
    c.execute(statement,{'user_id':userid})
    userinfo,= c.fetchall()
    usermail = userinfo[3]
    print(userinfo)

    if request.method == 'POST':
        message = ""
        oldpass = request.POST['password']
        username = request.POST.get('username')
        newpass = request.POST.get('newPassword')
        confirmpass = request.POST.get('confirmPassword')
        
        if(argon2.verify(oldpass,userinfo[2])):
            if username == userinfo[1] and newpass == "" and confirmpass == "":
                message = "No changes made"
            else:
                if newpass == confirmpass and newpass != "":
                    hash_pass = argon2.hash(newpass)
                    statement = 'UPDATE USERS SET password = :p , name = :u WHERE email = :e'
                    c.execute(statement,{'p':hash_pass,'u':username,'e':usermail})
                    message = 'User info updated'
                    oldpass = newpass
                elif newpass != confirmpass:
                    message = "New password didn't match!"
                elif username != userinfo[1]:
                   
                    statement = 'UPDATE USERS SET  name = :u WHERE email = :e'
                    c.execute(statement,{'u':username,'e':usermail})
                    
                    message = 'User info updated'
       


        else:
            message = "Password not verified"

        c.close()
        connection.commit()
        connection.close()
        return render(request,'accounts/settings.html',{'error':message,'userid':userid,'name':username,'password':oldpass,'usermail':usermail,'role':userinfo[0]})

        
    else:
        c.close()
        connection.close()
        return render(request,'accounts/settings.html',{'userid':userid,'role':userinfo[0],'name':userinfo[1],'password':userinfo[2],'usermail':usermail})



def students(request):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    userid = request.session['userid']
    role = request.session['role']

    statement = """SELECT C.NAME,C.CLASS,C.TOTAL_MARKS,COUNT(E.ST_ID),C.CREATION_TIME
                FROM COURSES C,ENROLL E,TAKE_COURSE T
                WHERE T.TEACHER_ID = :t AND C.ID = T.COURSE_ID  AND E.COURSE_ID(+) = C.ID
                GROUP BY (C.NAME,C.CLASS,C.TOTAL_MARKS,C.CREATION_TIME)"""

    c.execute(statement,{'t':userid})
    courseinfo = c.fetchall()
    
    statement = """SELECT S.NAME,S.EMAIL,C.NAME,C.CLASS,E.PERCENTAGE_COMPLETED,E.ENROLL_TIME,S.ID
                   FROM USERS S,COURSES C,ENROLL E,TAKE_COURSE T
                   WHERE T.TEACHER_ID = :t AND T.COURSE_ID = E.COURSE_ID AND
                   E.COURSE_ID = C.ID AND E.ST_ID = S.ID"""

    c.execute(statement,{'t':userid})
    enrollinfo = c.fetchall()
    c.close()
    connection.close()

    return render(request,'accounts/students.html',{'userid':userid,'role':role,'enrollinfo':enrollinfo,'courseinfo':courseinfo})


def progress(request):
    if request.session.has_key('userid') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    userid = request.session['userid']
    role = request.session['role']
    
    statement = """SELECT C.NAME,C.CLASS,E.PERCENTAGE_COMPLETED,E.ENROLL_TIME
                    FROM STUDENTS S,COURSES C,ENROLL E
                    WHERE S.ID = :t AND E.ST_ID = S.ID AND E.COURSE_ID = C.ID"""

    c.execute(statement,{'t':userid})
    enrollinfo = c.fetchall()
    c.close()
    connection.close()
    print(enrollinfo)

    return render(request,'accounts/progress.html',{'userid':userid,'role':role,'enrollinfo':enrollinfo})

def course_classes(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        role = request.session['role']
    else:
        userid = None
        role = None
    classes=[]
    for i in range(0,12):
        classes.append(i+1)
    return render(request,'accounts/course_classes.html',{'userid':userid,'role':role,'classes':classes})



"""


<div class="modal fade" id="test{{course.0}}" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header text-center">
                    
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                        </button>
                </div>
                <div class="modal-body mx-3">
                    <h5 class="modal-title w-100 font-weight-bold"  style="text-align:center">Delete this content permanently?</h5>
                    <form class="form-settings" action="{% url 'courses:del_course' course.0 %}" method="POST">
                    {% csrf_token %}
                    
                    
                    <div class="modal-footer d-flex justify-content-center">
                        <button class="btn btn-info btn-sm" type="submit">Confirm</button> 
                        
                    </div>
                  </form>
      
                </div>
                
            </div>
        
        </div>
    </div> 

      <div class="modal fade" id="contribute{{course.0}}" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header text-center">
                    
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                        </button>
                </div>
                <div class="modal-body mx-3">
                    <h5 class="modal-title w-100 font-weight-bold"  style="text-align:center">Add Contributor</h5>
                    <form class="form-settings" action="{% url 'courses:contribute_course' course.0 %}" method="POST">
                    {% csrf_token %}
                    
                    <div class="md-form mb-4">
                        <label data-error="wrong" data-success="right" for="mail">Contributor's Mail ID</label>
                        <input type="text" id='mail' name = 'mail' class="form-control validate" required>
                        
                    </div>

                    <div class="modal-footer d-flex justify-content-center">
                        <button class="btn btn-info btn-sm" type="submit">Confirm</button> 
                        
                    </div>
                  </form>
      
                </div>
                
            </div>
        
        </div>
      </div> 
    

    <div class="row  pt-3  mydiv " >
        
        
        <div class="col-md-3" style="pointer-events:auto" >
            <a href="#contribute{{course.0}}" data-toggle="modal">Add Contributor</a>
        </div>
        {% if course.5 == 'owner' %}
        <div class="col-md-3"style="pointer-events: auto;" >
            <a href="#test{{course.0}}" data-toggle="modal">Delete</a>
        </div>
        {% endif %}

           
    </div>
"""