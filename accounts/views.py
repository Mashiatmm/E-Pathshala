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
    
    if request.session.has_key('usermail'):
        usermail = request.session['usermail']
        return render(request,'accounts/home.html',{'usermail':usermail})
    return render(request,'accounts/home.html')


def signup(request,role):

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    
    c = connection.cursor()

    if request.method=='POST':
        
    
        if request.POST['password1']==request.POST['password2']:

            try:
                    
                hash_pass = argon2.hash(request.POST['password2'])
                statement = 'insert into USERS(name,email, password,role) values (:0,:1,:2,:3)'
                c.execute(statement, (request.POST['username'], request.POST['email'],hash_pass,role))
                
                c.execute("select id from USERS where email = :usermail",{'usermail':request.POST['email']})
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
                if request.session.has_key('usermail'):
                    del request.session['usermail']
                request.session['usermail'] = request.POST['email']
                return redirect('/accounts/profile',{'usermail':request.session['usermail']})
                #return render(request,'accounts/profile.html',{'id':val,'role':role,'name':request.POST['username'],'email':request.POST['email'],'password':request.POST['password2']})
            except:  
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

                if request.session.has_key('usermail'):
                    del request.session['usermail']

                request.session['usermail'] = email
                
                connection.close()
                return redirect('/accounts/profile',{'usermail':email})
                #return redirect('/accounts/'+info[1]+'/'+str(info[2]))

            else:
                c.close()
                connection.close()
                return render(request,'accounts/login.html',{'error':"Incorrect Password!!"})
                
    
    else:
        try:
            del request.session['usermail']
        except:
            pass
        return render(request,'accounts/login.html')



def profile(request):

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)

    if request.session.has_key('usermail'):
        usermail = request.session['usermail']

        c = connection.cursor()

        statement = "select role from USERS where email=:mail"
        c.execute(statement,{'mail':usermail})  
        role, = c.fetchone()
        if role=="student":
            statement="""Select U.ID AS "ID",U.NAME,S.CLASS 
                        FROM USERS U, STUDENTS S 
                        WHERE S.ID=U.ID AND U.EMAIL=:user_email"""
        else:
            statement="""Select  U.ID AS "ID",U.NAME,T.Specialty 
                        FROM USERS U, TEACHERS T
                        WHERE T.ID=U.ID AND U.EMAIL=:user_email"""

        c.execute(statement,{'user_email': usermail})
        user,=c.fetchall()
        c.close()
        #print(role,user[0],user[1],user[2],user[3])
        return render(request,'accounts/profile.html',{'usermail':usermail,'role':role,'name':user[1],'t_id':user[0]})
    
    else:
        return render(request,'accounts/login.html',{'error': 'Not Logged In'})


def settings(request):
    if request.session.has_key('usermail') == False:
            return render(request,'accounts/login.html',{'error': 'Not Logged In'})

    

    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    connection = cx_Oracle.connect(user='EPATHSHALA',password='123',dsn=dsn_tns)
    c = connection.cursor()

    usermail = request.session['usermail']
    statement = 'SELECT role,name,password FROM USERS WHERE email = : user_email'
    c.execute(statement,{'user_email':usermail})
    userinfo,= c.fetchall()
    
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
        return render(request,'accounts/settings.html',{'error':message,'usermail':usermail,'name':username,'password':oldpass})

        
    else:
        c.close()
        connection.close()
        return render(request,'accounts/settings.html',{'usermail':usermail,'role':userinfo[0],'name':userinfo[1],'password':userinfo[2]})


