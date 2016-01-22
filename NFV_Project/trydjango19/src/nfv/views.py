from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.core.context_processors import csrf
from trydjango19 import settings
from django.contrib.auth.decorators import login_required
# Create your views here.

# def login(request):
#    return render(request, "login.html", {})
 
def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)

def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.groups.filter(name="Developer").exists():        
        auth.login(request, user)
        return HttpResponseRedirect('/nfv/developer')
    elif user is not None and user.groups.filter(name="Admin_Users").exists():
        auth.login(request, user)
        return HttpResponseRedirect('/nfv/admin')
    elif user is not None and user.groups.filter(name="Enterprise").exists():
        auth.login(request, user)
        return HttpResponseRedirect('/nfv/enterprise')
    else:
        return HttpResponseRedirect('/nfv/invalid')
    
def invalid_login(request):
    return render_to_response('Invalid.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

def developer(request):
    return render_to_response('Developer.html', {'full_name': request.user.first_name})

def admin(request):
    return render_to_response('Admin.html', {'full_name': request.user.first_name})

def enterprise(request):
    return render_to_response('Enterprise.html', {'full_name': request.user.first_name})
# 
# def submit(request):
#    # next = request.GET.get{'next', /login/'}
#     #if request.method == "POST":
#      #   username = request.POST['username']
#     #    password = request.POST['password']
#     if request.POST:
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                   #return HttpResponseRedirect('nfv/developer')
#                 return HttpResponseRedirect('settings.DEVELOPER_URL')
#             else:
#                 return HttpResponseRedirect("Inactive User")
#         else:
#             return HttpResponseRedirect("Invalid username/password")
#     return render(request, "developer.html", {})
#         #HttpResponseRedirect('nfv/login')
#         
        

