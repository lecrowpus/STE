from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import models 
import random
from django.core.mail import send_mail
import time
# Create your views here.
def home(request):
    """
    here we are checking if the user is login or not for the logout and profile links to work in navebar in base.html .
    and rendering home.html page 
    """
    state=False
    user=None
    try:
        user=request.session['user'] #getting the user from session
        state=False #declaring the var for further use
    except:
        pass



    if user != None: # checking if the user is None or not to prevent error :QueryDosentMatch 
        data=models.users.objects.get(username=user) #getting the data of the user if is not None

        if data.state==True: #checking if user is logedin
            state=True # changeing the value of the state var to pass it in the base.html ofr logedin uses (eg. logout , profile )
            data.save() # saving the data for security measure
            request.session['state']=state 
    return HttpResponse(render(template_name="home.html",request=request,context={"state":state})) # rendering the homepage and sending the state var for logedin func \n
    # to work

def signuppage(request):
    """
    here we ar rendering the signup page to the user .
    """
    try:
        state=request.session["state"]
    except:
        state=None
    return HttpResponse(render(template_name="signup.html",request=request,context={"usernameteaken":1,"state":state})) # rendering signup page , the usernametaken var is to display 
    # the username already take msg to the user .(if else statements in html file)

def adduser(request):
    """
    here we are creating/registering a user and saving it to the database . redirecting if it was sucessfull
    if the username is already take sending client back to signup page with a warning 
    """
    x=request.POST['username']
    p=request.POST['password'] # getting the username , password , email from the form  
    e=request.POST['email']

    try:# trying to get the user data from the database to check if he exists
        data=models.users.objects.get(username=x)
 
    except (models.users.DoesNotExist):# if user doesNotExist the create/register the user 
        data=models.users(username=x,password=p,state=True,email=e) # creating/registering the user 
        data.save() # saving the user 
        request.session['user']=x # declaring or changing the user value in session from none to the username . for further use in checking the user is logedin or not 
        return HttpResponseRedirect("/") # redirecting to homepage after the user is created

    else:# if user allready exist in the database the send a warning to the signup .html
        return HttpResponse(render(template_name="signup.html",request=request,context={"usernameteaken":f"""This username is allready taken use other usernames
         like {x}123 or {x.upper()}  .If your trying to login please click ' Login> 'bellow ""","state":request.session["state"]})) #rendering the signup page with a warning

def loginpage(request):
    """
    checking if the user is allready logedin or not if yes then redirecting  him to homepage if no the rendering login page
    """
    state=None

    try: #trying if the user is None 
        x=request.session['user']#getting the user form session 
        data=models.users.objects.get(username=x) # getting the data of the user 
        state=request.session["state"]

        if data.state==True: # if the user is allready logedin the redirecting him to homepage
            return HttpResponseRedirect("/") #redirecting to home page

    except:# if user is none then passing out is 
        pass        
    return HttpResponse(render(template_name="login.html",request=request,context={"state":state})) # rendering the login page
    
def login(request):
    """
    checking the password and loging in the user if wrong password redirecting to login page 
    with a waring 
    """ 
    x=request.POST['username']
    p=request.POST['password'] # getting the username and passwod from the form 

    data=models.users.objects.get(username=x) # getting the data of the user 

    if data.state==True:# checking if the user is logedin  
        return HttpResponseRedirect("/")# rendering homepage cuz he is all ready logedin 

    if p==data.password:# checking the password 
        #pssword was correct!
        data.state=True #changing the state of the user to true
        data.save() #seving the Change
        url = reverse('index') # declaring the url
        request.session['user']=x #declering the user in session
        return HttpResponseRedirect(url) # redirecting to homepage

    if p!=data.password:# if the password was wrong sending back to loginpage with the warning
        return HttpResponse(render(template_name="login.html",request=request,context={"msg":"Wrong password please try againg or user emailverification","state":request.session["state"]})) # rendering the login page

def emailverificationpage(request):
    """
    sending the verification code to the user's email
    """
    x=request.session['user']#getting the user

    try:# if user is all ready logedin then redirecting to homepage
        data=models.users.objects.get(username=x) # geting the user data

        if data.state==True: #checking if he is logedin
            return HttpResponseRedirect("/")# redirecting to homepage

    except:# if error user is none then continuing
        pass
    
    x=request.POST['username']# geting the user name from the form
    request.session['loginuser']=x # setting the loging user to pass it ot verify func

    try:# trying if that user exist 
        data=models.users.objects.get(username=x)# getting the user data
    except:
        pass

    e=data.email#geting the email of the user

    code='' #declaring the code var for further user 

    for i in range(6): # generating the 6 digit code using random module 
        code=f"{code}{random.randint(0,9)}"# generating a random num from 0 to 9 and appending it to code var

    request.session['verification']=code # saving the code in session var

    send_mail( # sending the mail
        'login through email verification ',
        f'Hi, This is from classhub .com . your are trying to loging through email verification. \n The Verification code is  [{code}]',
        "emailclasshub@gmail.com",
        [e],
        fail_silently=False,
    )

    request.session['time'] = time.time() # declaring the time var , the value is unix time echop
    
    #rendering emailverification page with action var which is used in form action (this page is used be other func)
    return HttpResponse(render(template_name="emailverifaction.html",request=request,context={"action":"/verify","state":request.session["state"]}))

def verify(request):

    """getting the otp from the user and from the session (from emailverificatinpage func) and validating it  if 
    its valid then loging in the user """
    x=request.session['user']# getting the user from the session
   
    try:# checking if the user is allready logedin 
        data=models.users.objects.get(username=x)# geting the user data

        if data.state==True:# checking if he is logedin 
            return HttpResponseRedirect("/")# redirecting to home page
    except:# error if user is Nonee
        pass
    
    curr = time.time()# getting the current time from unix time echop
    curr2=request.session['time'] # getting the time of email send in unxi time echop 
    
    #converting time into int
    curr2=int(curr2)
    curr=int(curr)

    if curr-curr2 > 60:# checking if the difference between time if the code is valid or not
        # if not ,return to home page with a warning
        return HttpResponse(render(template_name="login.html",request=request,context={"msg":f"Time Out you must enter the code under 60 sec","state":request.session["state"]}))

    c=request.POST['otp'] # getting the otp user has enterd
    c=int(c)# converting otp into int

    c2=request.session['verification']# geting the verification code
    c2=int(c2)# converting otp into int

    if c==c2:#checking if otp is correct
        x=request.session['loginuser']# geting the login user
        request.session['loginuser']=None
        request.session['verification']=None# setting the unwanted vars to None
        request.session['time']=None
        
        request.session['user']=x# setting the user in session
        data=models.users.objects.get(username=x) # geting the user data
        data.state=True # loging in the user
        data.save() # seving the change
        return HttpResponseRedirect("/") # redirecting user to home page
    # if something went wrong rendering login page and a warning    
    return HttpResponse(render(template_name="login.html",request=request,context={"msg":f"something went wrong try please again","state":request.session["state"]}))

def logout(request):
    """simply logingout user by changing its state"""
    user=request.session['user']# getting user
    data=models.users.objects.get(username=user)# getting user data
    data.state=False # logouting user
    data.save()#saving change

    request.session['user']=None # removing user from session
    return HttpResponseRedirect("/")# redirecting to homepage

def profilepage(request):
    #rendering profile page
    return HttpResponse(render(template_name="profile.html",request=request,context={"state":request.session["state"]}))

def changemail(request):
    e=request.POST['email']# geting the new email 
    
    p=request.POST['password'] # geting password and username
    u=request.session['user']

    data=models.users.objects.get(username=u) #getting userdata
    password=data.password

    if p==password:#checking password
        data.email=e# changeing email
        data.save()#saving change
        # rendering profile page with a sucess msg
        return HttpResponse(render(template_name="profile.html",request=request,context={"msg":"Email changed sucessfuly !","state":request.session["state"]}))
    else:   
        # rendering profile page and a warning  
        return HttpResponse(render(template_name="profile.html",request=request,context={"msg":"Wrong password","state":request.session["state"]}))
        
def changep(request):

    request.session['npassword']=request.POST['password']# settiong new password
    x=request.session['user']# getting user    
    data=models.users.objects.get(username=x)#getting user data
    e=data.email

    code=''# defining code

    for i in range(6):#generating code
        code=f"{code}{random.randint(1,9)}"

    request.session['verification']=code# definfng sessing code

    send_mail(# sending code 
        'login through email verification ',
        f'Hi, This is from classhub .com . your are trying to change password through email verification. \n The Verification code is  [{code}]',
        "emailclasshub@gmail.com",
        [e],
        fail_silently=False,
    )
    request.session['time'] = time.time() # getting unix time echop
    # rendering emailverification page with action cuz other func are using same page
    return HttpResponse(render(template_name="emailverifaction.html",request=request,context={"action":"/verifypassword","state":request.session["state"]}))

def verifyp(request):
    x=request.session['user']# getting user 

    data=models.users.objects.get(username=x)# getting user data

    curr = time.time() # getting current unix echop time 
    curr2=request.session['time'] #  getting unix time echop (from sending email)
    
    curr2=int(curr2)# converiting them into int
    curr=int(curr)
    
    if curr-curr2 > 60:# checking time valadation
        # rendering login page with time out msg
        return HttpResponse(render(template_name="login.html",request=request,context={"msg":f"Time Out you must enter the code under 60 sec","state":request.session["state"]}))

    c=request.POST['otp'] # getting and typecasting it into int
    c=int(c)
    c2=request.session['verification']
    c2=int(c2)

    if c==c2:#checking the otp
        request.session['loginuser']=None
        request.session['verification']=None# nulling unwanted session var
        request.session['time']=None
       
        request.session['user']=x # getting session user

        data=models.users.objects.get(username=x)# getting user data
        data.password=request.session['npassword']# getting new password
        request.session['npassword']=None#  nulling unwanted session var
        data.save()# saving change
        return HttpResponseRedirect("/")# redirecting to home page
    # rendering profile page with a warning
    return HttpResponse(render(template_name="profile.html",request=request,context={"msg":f"something went wrong try please again","state":request.session["state"]}))



    
    
