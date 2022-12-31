from django.urls import path
from . import views
urlpatterns = [
    path('',views.home ,name="index"),
    path('signup',views.signuppage ),
    path('adduser',views.adduser ),
    path('logedin',views.login ),
    path('login',views.loginpage ),
    path('emailvpage',views.emailverificationpage),
    path('verify',views.verify),
    path('logout',views.logout),
    path('profile',views.profilepage,name="profile"),
    path('changeE',views.changemail),
    path('changep',views.changep),
    path('verifypassword',views.verifyp),
    
    
]
