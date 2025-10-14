from django.shortcuts import render,redirect
from .models import Teacher
from .models import Student
# Create your views here.
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate,login,logout


def RegisterView(request):
    if request.method=="POST":
        data=request.POST
        username=data['username']
        password=data["password"]
        email=data["email"]
        role=data["role"].lower()
        if User.objects.filter(username=username).exists():
            messages.error(request,"username already exist")
            return redirect('register')
        user=User.objects.create_user(username=username,password=password,email=email,role=role)
        
        if role=='student':
            st=Student.objects.create(user=user)
            st.save()
        if role=='teacher':
            tt=Teacher.objects.create(user=user)
            tt.save()
        messages.success(request,"successfully created the user")
        return redirect('register')
        


    return render(request,"register.html")



def loginView(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        role=request.POST.get("role")
        user=request.user.authenticate(username=username,password=password,role=role)
        if user is not None:
            pass
    return render(request,"login.html")




