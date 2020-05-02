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
                user=User.objects.create_user(username=request.POST['username'],email=request.POST['email'],password=request.POST['password2'])
                auth.login(request,user)
                return redirect('home')#redirecting to a url

        
        else:
            return render(request,'accounts/signup.html',{'error':"Passwords didn't match!"})
    
    else:
        return render(request,'accounts/signup.html')

    
