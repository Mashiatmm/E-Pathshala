from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import auth
import cx_Oracle

def home(request):
    return render(request,'accounts/home.html')


def signup(request):

    if request.method=='POST':
        dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
        conn = cx_Oracle.connect(user='hr',password='hr',dsn=dsn_tns)
        c = conn.cursor()
    
        if request.POST['password1']==request.POST['password2']:
            

            statement = 'select email from USERS where email = :mail_id'
            c.execute(statement, {'mail_id': request.POST['email']})
            mail_exists = c.fetchall()

            if mail_exists is None:

                statement = 'select name from USERS where name = :username'
                c.execute(statement, {'username': request.POST['username']})
                name_exists = c.fetchall()

                if name_exists is None:

                    count=conn.cursor()
                    count.execute("select count(*) from USERS")
                    val,=count.fetchone()
                    statement = 'insert into USERS(id,name,email, password,role) values (:1,:2, :3, :4,:5)'
                    c.execute(statement, (val, request.POST['username'], request.POST['email'],request.POST['password2'],'teacher'))

                    conn.commit()
                    conn.close()
                    return redirect('home')#redirecting to a url                 

                else:
                    conn.close()
                    return render(request,'accounts/signup.html',{'error':"Username already taken!"})



            else:    
                conn.close()
                return render(request,'accounts/signup.html',{'error':"Email already taken!"})
        
        else:
            return render(request,'accounts/signup.html',{'error':"Passwords didn't match!"})
    
    else:
        return render(request,'accounts/signup.html')


def login(request):
    if request.method=='POST':
        try:
            user=User.objects.get(email=request.POST['email'])
            
        except User.DoesNotExist:
            try:
                user=User.objects.get(username=request.POST['email'])  
                   
            except User.DoesNotExist:
                return render(request,'accounts/login.html',{'error':"User Does Not Exist!!!"})
        if check_password(request.POST['password'], user.password):
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'accounts/login.html',{'error':"Password didn't match!"})
       
            

    else:
        return render(request,'accounts/login.html')


    


    
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