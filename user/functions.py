from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import models 
import random
from django.core.mail import send_mail
import time


def usercheck(request):
    x=request.session['user']
    try:
        data=models.users.objects.get(username=x)
        if data.state==True:
            return HttpResponseRedirect("/")
    except:
        return False 
def emailverification(request,msg,to ,sub):
    x=request.session['user']
    try:
        data=models.users.objects.get(username=x)
        if data.state==True:
            return None
    except:
        pass
    x=request.POST['username']

    code=''
    for i in range(6):
        code=f"{code}{random.randint(1,9)}"
    print(code)   
    request.session['verification']=code

    send_mail(
        sub,
        msg,
        "emailclasshub@gmail.com",
        [to],
        fail_silently=False,
    )
    request.session['time'] = time.time()
    return True