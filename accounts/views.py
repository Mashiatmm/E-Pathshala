from django.shortcuts import render,redirect
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.db import connection
import cx_Oracle
from passlib.hash import argon2


#Mashiat Virtual Env - 'myvenv'

def home(request):
    '''
    c = connection.cursor()
    statement = 'select id,password from USERS'
    c.execute(statement)
    passwords = c.fetchall()
  
    
    for i in range(len(passwords)):
        hash_pass = argon2.hash(passwords[i][1])
       
        statement = 'update USERS set password = :p where id = :i '
        c.execute(statement, {'p': hash_pass, 'i': passwords[i][0]})
    
    c.close()
    '''
    return render(request,'accounts/home.html')


def signup(request,role):
    '''
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    conn = cx_Oracle.connect(user='hr',password='hr',dsn=dsn_tns)
    '''
    c = connection.cursor()

    if request.method=='POST':
        
    
        if request.POST['password1']==request.POST['password2']:
            statement = 'select email from USERS where email = :mail_id'
            c.execute(statement, {'mail_id': request.POST['email']})
            mail_exists = c.fetchall()
    

            if mail_exists == [] :
                    
                print(request.POST['username'], request.POST['email'],request.POST['password2'],role)
                hash_pass = argon2.hash(request.POST['password2'])
                statement = 'insert into USERS(name,email, password,role) values (%s,%s, %s,%s)'
                c.execute(statement, (request.POST['username'], request.POST['email'],hash_pass,role))
                
                count=connection.cursor()
                count.execute("select id from USERS where email = :usermail",{'usermail':request.POST['email']})
                val,=count.fetchone()
                count.close()

                
                if role== 'student':
                    statement='insert into STUDENTS(id,class) values (%s,%s)'
                    c.execute(statement,(val,request.POST['grade']))
                    
                else:
                    statement='insert into TEACHERS(id,specialty) values (%s,%s)'
                    c.execute(statement,(val,request.POST['specialty']))
                
                
                
                connection.commit()
                c.close()

                
                return render(request,'accounts/profile.html',{'id':id,'role':role,'name':request.POST['username'],'email':request.POST['email'],'password':request.POST['password2']})
            else:    
                c.close()
                return render(request,'accounts/signup.html',{'role':role,'error':"Email already taken!"})
        
        else:

            return render(request,'accounts/signup.html',{'role':role,'error':"Passwords didn't match!"})
    
    else:
        if role == 'student':
            c.close()
            return render(request,'accounts/signup.html',{'role':role})
        else:
            statement='select distinct specialty from TEACHERS'
            c.execute(statement)
            all_spec=c.fetchall()
            all_specialties=[]
            for spec in all_spec:
                all_specialties.append(spec[0])
            c.close()
            return render(request,'accounts/signup.html',{
                'role':role,
                'all_specialties':all_specialties
            })

        


def login(request):
    if request.method=='POST':
        '''
        dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
        conn = cx_Oracle.connect(user='hr',password='hr',dsn=dsn_tns)
        '''
        c = connection.cursor()
        email= request.POST['email_or_name']
        statement= 'select email from USERS where email=:mail'
        c.execute(statement,{'mail':email})
        user_exists=c.fetchall()

        if user_exists == [] :
            c.close()
            return render(request,'accounts/login.html',{'error':"Mail ID Does Not Exist!!!"})

        else:
            statement="select password,role,id from USERS where email=:mail"
            c.execute(statement,{'mail':email})
            info= c.fetchone()

            if(argon2.verify(request.POST['password'],info[0])):
                c.close()
                return redirect('/accounts/'+info[1]+'/'+str(info[2]))

            else:
                c.close()
                return render(request,'accounts/login.html',{'error':"Incorrect Password!!"})
                
    
    else:
        return render(request,'accounts/login.html')



def profile(request,role,id):
    '''
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    c = cx_Oracle.connect(user='hr',password='hr',dsn=dsn_tns)
    '''
    c = connection.cursor()
    print(role,id)
    statement=""
    if role=="student":
        statement="""Select U.ID AS "ID",U.NAME,U.EMAIL,U.PASSWORD,S.CLASS 
                    FROM USERS U, STUDENTS S 
                    WHERE S.ID=U.ID AND U.ID=:userid"""
    else:
        statement="""Select  U.ID AS "ID",U.NAME,U.EMAIL,U.PASSWORD,T.Specialty 
                    FROM USERS U, TEACHERS T
                    WHERE T.ID=U.ID AND U.ID=:userid"""

    c.execute(statement,{'userid':id})
    user,=c.fetchall()
    c.close()
    return render(request,'accounts/profile.html',{'role':role,'name':user[1],'email':user[2],'password':user[3],'t_id':id})


