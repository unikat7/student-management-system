from django.shortcuts import render,redirect
from .models import Teacher
from .models import Student
# Create your views here.
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.http import HttpResponse
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
        role=request.POST.get("role").lower()
        user=authenticate(username=username,password=password,role=role)
        if user is not None:
            refresh=RefreshToken.for_user(user)
            refresh['role']=role
            response=redirect(f"{role}")
            response.set_cookie(
                key='jwt',
                value=str(refresh.access_token),
                httponly=True,
                samesite='Lax'
            )
            messages.success(request,f"successfully login as {role}")
            return response
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request,"login.html")


def studentdashboard(request):
    token=request.COOKIES.get('jwt')
    if not token:
        return redirect('login')
    auth=JWTAuthentication()
    try:
        validated_token = auth.get_validated_token(token)  
        user = auth.get_user(validated_token)
        request.user = user
    except AuthenticationFailed:
        return redirect('login')
    if validated_token.get('role') != 'student':
        return HttpResponse("Unauthorized: Only students allowed", status=403)
    return render(request,"studentdash.html",{
        "user":user
    })



def teacherdashboard(request):
    token=request.COOKIES.get('jwt')
    if not token:
        return redirect('login')
    auth=JWTAuthentication()
    try:
        validated_token = auth.get_validated_token(token)  
        user = auth.get_user(validated_token)
        request.user = user
    except AuthenticationFailed:
        return redirect('login')
    if validated_token.get('role') != 'teacher':
        return HttpResponse("Unauthorized: Only students allowed", status=403)

    return render(request,"teacherdash.html",{
        "user":user
    })




