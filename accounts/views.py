from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import auth

def home(request):
    return render(request,'accounts/home.html')\


def signup(request):
    if request.method=='POST':
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.get(email=request.POST['email'])
                return render(request,'accounts/signup.html',{'error':"Email already taken!"})

            except User.DoesNotExist:
                try:
                    user=User.objects.get(username=request.POST['username'])
                    return render(request,'accounts/signup.html',{'error':"Username already taken!"})
                except User.DoesNotExist:
                    user=User.objects.create_user(username=request.POST['username'],email=request.POST['email'],password=request.POST['password2'])
                    auth.login(request,user)
                    return redirect('home')#redirecting to a url                 
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