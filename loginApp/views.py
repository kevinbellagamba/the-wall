from django.http.response import Http404, HttpResponse
from .models import User
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

# Create your views here.
from django.shortcuts import render, redirect
def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            print(request.POST['password'])
            print(hashedpw)
            newUser = User.objects.create( 
            first_name=request.POST['first_name'], 
            last_name=request.POST['last_name'], 
            email_address=request.POST['email_address'], 
            password= hashedpw)
            request.session['user'] = newUser.id
            return redirect('/success') 
    else:
        return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            LoggedUser = User.objects.get(email_address=request.POST['log_email_address'])
            request.session['user'] = LoggedUser.id
            return redirect("/success")
    else:
        return redirect('/')

def success(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id=request.session['user'])
    }
    return redirect('/wall')
    

def logout(request):
    request.session.flush()
    return redirect('/')

def users(request):
    context = {
        'users' : User.objects.all(),
    }
    return render(request, "users.html", context)