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
        print('Recieved1\n')
        
    
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
                    count.execute("select max(id) from USERS")
                    val,=count.fetchone()
                    val+=1
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
                    return redirect('home')
                else:
                    conn.close()
                    return render(request,'accounts/signup.html',{
                        'error':"Username already taken!",
                        'role':role
                        
                        })



            else:    
                conn.close()
                return render(request,'accounts/signup.html',{
                    'error':"Email already taken!",
                    'role':role
                    
                    })
        
        else:

            return render(request,'accounts/signup.html',{
                'error':"Passwords didn't match!",
                'role':role
                })
    
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
        statement= 'select email from USERS where email=:mail_id'
        c.execute(statement,{'mail_id':email_or_name})
        mail_exists=c.fetchall()
        if mail_exists == [] :
            statement= 'select name from USERS where name=:username'
            c.execute(statement,{'username':email_or_name})
            name_exists=c.fetchall()
            if name_exists == []:
                conn.close()
                return render(request,'accounts/login.html',{'error':"User Does Not Exist!!!"})
            else:
                conn.close()
                return redirect('home')
                

        else:
            conn.close()
            return render(request,'accounts/login.html',{'error':"User Does Not Exist!!!"})
                
    
    else:
        return render(request,'accounts/login.html')


'''
if request.method=='POST':
        try:
            user=User.objects.get(email=request.POST['email_or_name'])
            
        except User.DoesNotExist:
            try:
                user=User.objects.get(username=request.POST['email_or_name'])  
                   
            except User.DoesNotExist:
                return render(request,'accounts/login.html',{'error':"User Does Not Exist!!!"})
        if check_password(request.POST['password'], user.password):
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'accounts/login.html',{'error':"Password didn't match!"})
       
            


'''


    
'''
if request.method=='POST':#if inside the page anything is posted ie name and password
        user=auth.authenticate(email=request.POST['email'],password=request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else :
            return render(request,'accounts/login.html',{'error':'email or password is wrong!'})
               
    else:#if a get request ie the page is requested via the url
        return render(request,'accounts/login.html')
'''