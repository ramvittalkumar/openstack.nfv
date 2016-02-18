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
from django.template import RequestContext
from django.shortcuts import render
import json
import requests


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

# def my_custom_sql():
#     cursor = connections['nfv'].cursor()
#    # cursor = connection.cursor()
#
#     cursor.execute("SELECT User_Id, User_Type,First_Name FROM VNF_User")
#     results = namedtuplefetchall(cursor)
#
#     for row in results :
#         print "User Id " +str(row.User_Id)
#         print "User Type " +str(row.User_Type)
#         row = cursor.fetchone()
#     #print results[0][0]
#     #print results[0].User_Id
#
#     # data = cursor.fetchall()
#     # for row in data :
#     #     print row[0].User_Id
#     #     row = cursor.fetchone()
#
#     cursor.close()
#
#     return results


# Create your views here.

 
def login(request):
    c = {}
    c.update(csrf(request))
    
    return render_to_response('login.html', c)

def login_auth(request):

    username = request.POST.get('username','')
    password = request.POST.get('password','')

    url='http://192.168.1.6:8081/login/loginHandler/'+username+'/'+password

    # if resp.status_code!=200:
    #     raise ApiError(resp.status_code)

    resp=requests.get(url)
    item = resp.json()

    if item['UserRole']=="Developer":
        return HttpResponseRedirect('/nfv/developer')
    elif item['UserRole']=="admin":
        return HttpResponseRedirect('/nfv/admin')
    elif item['UserRole']=="Enterprise":
        return HttpResponseRedirect('/nfv/enterprise')
    else:
        return HttpResponseRedirect('/nfv/invalid')

def CreateVNF(request):

    print("Create VNF")

    vnfName= request.POST.get('txtvnfName','')
    vnfDesc = request.POST.get('txtDescription','')
    imgLoc = request.POST.get('txtImageLocation','')
    vnfDef = request.POST.get('vnfDefinition','')
    vnfConfig = request.POST.get('Config','')
    vnfParam = request.POST.get('ParameterValuePoint','')

    # upload_api='http://192.168.1.6:8081/admin/uploadVNF/'
    #
    # imgLoc='/Users/cccuser/sample.txt'
    #
    # finalurl=upload_api+imgLoc
    #
    # print(finalurl)
    #
    # resp1= requests.get(finalurl)
    # item1=resp1.json()
    #
    # print(item1)

    print('UploadVNF success')

    dev_api= 'http://192.168.1.6:8081/developer/create/'

    url=dev_api+vnfName+'/'+vnfDesc+'/'+imgLoc+'/'+vnfDef+'/'+vnfConfig+'/'+vnfParam

    print(url)

    resp=requests.get(url)
    item = resp.json()

    if item['CatalogId']!=None:
        print "Success"
        return HttpResponseRedirect('/nfv/developer')

def listVNF(request):

    print("Listing VNF")

    admin_api='http://192.168.1.6:8081/admin/listCatalog'

    print(admin_api)
    resp=requests.get(admin_api)
    item = resp.json()
    obj = item['catalogs']
    for row in obj:
        print row['catalog']



    print(str(obj))

    return render(request, 'Admin.html' )










# def auth_view(request):
#     username = request.POST.get('username','')
#     password = request.POST.get('password','')
#
#     cursor = connections['nfv'].cursor()
#
#     sql = "SELECT User_Id, User_Type,First_Name FROM VNF_User where User_Id ="+username+" AND Password='"+password+"'"
#     print 'sql:'+sql
#     cursor.execute(sql)
#     results = namedtuplefetchall(cursor)
#
#     for row in results :
#         if row.User_Type=="Developer":
#             role= "Developer"
#             #return HttpResponseRedirect('/nfv/developer')
#         elif row.User_Type=="admin":
#             role="admin"
#             #return HttpResponseRedirect('/nfv/admin')
#         elif row.User_Type=="Enterprise":
#             role="Enterprise"
#             #return HttpResponseRedirect('/nfv/enterprise')
#         else:
#             role="Invalid"
#             #return HttpResponseRedirect('/nfv/invalid')
#         row = cursor.fetchone()
#         cursor.close()
#         return HttpResponse(role)
#

def invalid_login(request):
    return render_to_response('Invalid.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

def developer(request):
    #return render_to_response('Developer.html', {'full_name': request.user.first_name})
    return render_to_response('Developer.html',context_instance=RequestContext(request))

def admin(request):
    #return render_to_response('Admin.html', {'full_name': request.user.first_name})
    return render_to_response('Admin.html', context_instance=RequestContext(request))

def enterprise(request):
    #return render_to_response('Enterprise.html', {'full_name': request.user.first_name})
    return render_to_response('Enterprise.html', context_instance=RequestContext(request))





        

