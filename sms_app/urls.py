from django.urls import path
from .views import RegisterView,loginView
urlpatterns = [
    path('',RegisterView,name="register"),
    path('login/',loginView,name="login")
]
