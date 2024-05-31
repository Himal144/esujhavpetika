from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect 
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout 
from .forms import signupform

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Organization

def organization_detail(request, id):
    organization = get_object_or_404(Organization, id=id)
   
    context = {
        'organization': organization,
        'organization_url': f"http://127.0.0.1:8000/organization/{organization.id}/"
    }
    return render(request, 'organization/organization.html', context)

def baseapp (request):
    return render(request,'organization/base.html')

def login_form(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                messages.success(request,"Logged in successfully")
                return HttpResponseRedirect("/")
             
    else:
        fm = AuthenticationForm()
    
    context = {"loginform": fm}
    return render(request, "organization/login.html", context)

def signup_form(request):
    if request.method == "POST":
        fm = signupform(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Account Created successfully')
            fm = AuthenticationForm()
            context = {"loginform": fm}
            return render(request, "organization/login.html", context)
        else:
            return render(request, 'organization/signup.html', {'signupform': fm})
    else:
        fm = signupform()
        return render(request, 'organization/signup.html', {'signupform': fm})

def user_logout(request):
    logout(request)
    messages.warning(request,"Log out succefully")
    return HttpResponseRedirect('/')
