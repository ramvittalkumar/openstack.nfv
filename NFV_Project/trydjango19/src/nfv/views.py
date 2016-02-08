from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.core.context_processors import csrf
from trydjango19 import settings
from django.contrib.auth.decorators import login_required
import MySQLdb
from django.db import connections
from collections import namedtuple

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def my_custom_sql():
    cursor = connections['nfv'].cursor()
   # cursor = connection.cursor()

    #cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])

    #cursor.execute("SELECT * FROM NFV_Dev.VNF_User WHERE User_Id = %s", [self.User_Id])
    #cursor.execute("SELECT * FROM NFV_Dev.VNF_User ")
    #rows = cursor.fetchall()
    #cursor.fetchall()
    
    cursor.execute("SELECT User_Id, User_Type,First_Name FROM VNF_User")
    results = namedtuplefetchall(cursor)
    
    for row in results :
        print "User Id " +str(row.User_Id)
        print "User Type " +str(row.User_Type)
        row = cursor.fetchone()
    #print results[0][0]
    #print results[0].User_Id
    
    # data = cursor.fetchall()
    # for row in data :
    #     print row[0].User_Id
    #     row = cursor.fetchone()
    
    cursor.close()
    
    #for row in rows: print row.User_Id, row.User_Type,row.First_Name
    
    #for row in rows: print row.User_Id, row.User_Type
    # print row
    #print rows
    return results


#conn = MySQLdb.connect

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
    my_custom_sql()
    # cursor = connections['nfv'].cursor()
    # cursor.execute("SELECT User_Id, User_Type,First_Name FROM VNF_User where User_Id='131884' and Password='test123'")
    # 
    # data = cursor.fetchall()
    # for row in data :
    #     print row[0], row[1]
    #     row = cursor.fetchone()
    # if row[1]=="Developer":
    #     return HttpResponseRedirect('/nfv/developer')
    # elif row[1]=="admin":
    #     return HttpResponseRedirect('/nfv/developer')
    # elif row[1]=="Enterprise":
    #     return HttpResponseRedirect('/nfv/enterprise')
    # else:
    #     return HttpResponseRedirect('/nfv/invalid')
    # 
    # cursor.close()
    # return row
    #cursor.close()
    
    #user = auth.authenticate(username=username, password=password)

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
        

