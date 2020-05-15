from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import auth
import cx_Oracle

def home(request):
    return render(request,'accounts/home.html')


def signup(request,role):
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    conn = cx_Oracle.connect(user='hr',password='hr',dsn=dsn_tns)
    c = conn.cursor()

    if request.method=='POST':
        print('Received\n')
        
    
        if request.POST['password1']==request.POST['password2']:
            statement = 'select email from USERS where email = :mail_id'
            c.execute(statement, {'mail_id': request.POST['email']})
            mail_exists = c.fetchall()
    

            if mail_exists == [] :

                statement = 'select name from USERS where name = :username'
                c.execute(statement, {'username': request.POST['username']})
                name_exists = c.fetchall()

                if name_exists == []:

                    count=conn.cursor()
                    count.execute("select count(*) from USERS")
                    val,=count.fetchone()
                    statement = 'insert into USERS(id,name,email, password,role) values (:1,:2, :3, :4,:5)'
                    c.execute(statement, (val, request.POST['username'], request.POST['email'],request.POST['password2'],role))
                    
                    
                    if role== 'student':
                        statement='insert into STUDENT(id,grade) values (:1,:2)'
                        c.execute(statement,(val,request.POST['grade']))
                    
                    else:
                        statement='insert into TEACHER(id,specialty) values (:1,:2)'
                        c.execute(statement,(val,request.POST['specialty']))
                    
                    
                    conn.commit()
                    conn.close()
                    
                    return render(request,'accounts/profile.html',{'role':role,'name':request.POST['username'],'email':request.POST['email'],'password':request.POST['password2']})
                else:
                    conn.close()
                    return render(request,'accounts/signup.html',{'error':"Username already taken!"})



            else:    
                conn.close()
                return render(request,'accounts/signup.html',{'error':"Email already taken!"})
        
        else:

            return render(request,'accounts/signup.html',{'error':"Passwords didn't match!"})
    
    else:
        if role == 'student':
            conn.close()
            return render(request,'accounts/signup.html',{'role':role})
        else:
            statement='select distinct specialty from TEACHER'
            c.execute(statement)
            all_spec=c.fetchall()
            all_specialties=[]
            for spec in all_spec:
                all_specialties.append(spec[0])
            conn.close()
            return render(request,'accounts/signup.html',{
                'role':role,
                'all_specialties':all_specialties
            })

        


def login(request):
    if request.method=='POST':
        dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
        conn = cx_Oracle.connect(user='hr',password='hr',dsn=dsn_tns)
        c = conn.cursor()
        email_or_name= request.POST['email_or_name']
        password=request.POST['password']
        statement= 'select name from USERS where email=:username or name=:username'
        c.execute(statement,{'username':email_or_name})
        user_exists,=c.fetchone()

        if user_exists == [] :
            conn.close()
            return render(request,'accounts/login.html',{'error':"User Does Not Exist!!!"})

        else:
            statement="select password,role,id from USERS where name=:username"
            c.execute(statement,{'username':user_exists})
            info= c.fetchone()
        
            if(password==info[0]):
                conn.close()
                return redirect('/accounts/'+info[1]+'/'+str(info[2]))

            else:
                conn.close()
                return render(request,'accounts/login.html',{'error':"Incorrect Password!!"})
                
    
    else:
        return render(request,'accounts/login.html')



def profile(request,role,id):
    
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    conn = cx_Oracle.connect(user='hr',password='hr',dsn=dsn_tns)
    c = conn.cursor()
    print(role,id)
    statement=""
    if role=="student":
        statement="""Select USERS.ID AS "ID",NAME,EMAIL,PASSWORD,GRADE 
                    FROM USERS 
                    JOIN STUDENT 
                    on STUDENT.ID=USERS.ID 
                    where USERS.ID=:userid"""
    else:
        statement="""Select USERS.ID AS "ID",NAME,EMAIL,PASSWORD,Specialty 
                    FROM USERS 
                    JOIN TEACHER 
                    on TEACHER.ID=USERS.ID 
                    where USERS.ID=:userid"""

    c.execute(statement,{'userid':id})
    user,=c.fetchall()
    return render(request,'accounts/profile.html',{'role':role,'name':user[1],'email':user[2],'password':user[3]})


