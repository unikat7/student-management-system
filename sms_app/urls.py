from django.urls import path

from .views import RegisterView,loginView,teacherdashboard,studentdashboard,protected

urlpatterns = [
    path('',RegisterView,name="register"),
    path('login/',loginView,name="login"),
    path('teacher/',teacherdashboard,name='teacher'),
    path('student/',studentdashboard,name='student'),
    path('protected/',protected,name='protected')

]
