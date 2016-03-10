from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connections
from collections import namedtuple
from django.template import RequestContext
from django.shortcuts import render
import json
import requests
import random
import urllib


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

    url = 'http://192.168.1.8:8001/login/loginHandler/' + username + '/' + password
    print url
    resp=requests.get(url)
    item = resp.json()

    print('User Role:' + item['UserRole'])
    print item
    if item['UserRole']=="Developer":
        #username = {'Ram'}
        request.session['name'] = item['UserName']
        return HttpResponseRedirect('/nfv/developer')
        #return HttpResponseRedirect('/nfv/developer',{"username":username})
        #return render(request, '/nfv/developer', {"username": username},content_type="application/xhtml+xml" )
    elif item['UserRole']=="admin":
        #username = 'Ben'
        #return HttpResponseRedirect('/nfv/admin' + '?username')
        request.session['name'] = item['UserName']
        return HttpResponseRedirect('/nfv/admin')
      #  return render(request, '/nfv/admin', {"username": username},content_type="application/xhtml+xml" )
    elif item['UserRole']=="enterprise":
        request.session['name'] = item['UserName']
        return HttpResponseRedirect('/nfv/enterprise')
    else:
        return HttpResponseRedirect('/nfv/invalid')

def deleteCatalog(request):
    catalogId = request.POST.get('catalogId')
    url = 'http://192.168.1.8:8001/admin/delete/' + catalogId
    resp=requests.get(url)
    messages.error(request, 'Catalog deleted successfully')
    return HttpResponseRedirect('/nfv/admin')


def CreateVNF(request):
    ip = 'http://192.168.1.8:8001'
    print("Create VNF")

    vnfName= request.POST.get('txtvnfName','')
    vnfDesc = request.POST.get('txtDescription','')
    imgLoc = request.POST.get('txtImageLocation','')
    # vnfDef = request.POST.get('vnfDefinition','')
    # vnfConfig = request.POST.get('Config','')
    # vnfParam = request.POST.get('ParameterValuePoint','')
    if imgLoc == '':
        imgLoc = 'NA'

    if 'ImageFile' in request.FILES:
        path = handle_uploaded_file(request.FILES['ImageFile'])
        r = requests.post(ip + '/admin/uploadImage', files={'path': open(path, 'rb')})
        obj = r.json()
        imagePath = obj['path']
        imageName = request.FILES['ImageFile'].name
    else:
        messages.error(request, 'Please provide image file')
        return HttpResponseRedirect('/nfv/developer')

    if 'vnfDefinition' in request.FILES:
        path = handle_uploaded_file(request.FILES['vnfDefinition'])
        r = requests.post(ip + '/admin/toscaValidate', files={'path': open(path, 'rb')})
        obj = r.json()
        if obj['status'] != 'success':
            messages.error(request, 'Invalid (' + request.FILES[
                'vnfDefinition'].name + ') file - Not Compliant to TOSCA Standards')
            return HttpResponseRedirect('/nfv/developer')
        else:
            r = requests.post(ip + '/admin/toscaTranslate', files={'path': open(path, 'rb')})
            obj = r.json()
            vnfDefinitionPath = obj['path']
            vnfDefinitionName = request.FILES['vnfDefinition'].name
    else:
        vnfDefinitionPath = 'None'
        vnfDefinitionName = 'None'

    if 'Config' in request.FILES:
        path = handle_uploaded_file(request.FILES['Config'])
        r = requests.post(ip + '/admin/toscaValidate', files={'path': open(path, 'rb')})
        obj = r.json()
        if obj['status'] != 'success':
            messages.error(request, 'Invalid (' + request.FILES['Config'].name + ') file - Not Compliant to TOSCA Standards.')
            return HttpResponseRedirect('/nfv/developer')
        else:
            r = requests.post(ip + '/admin/toscaTranslate', files={'path': open(path, 'rb')})
            obj = r.json()
            configPath = obj['path']
            configName = request.FILES['Config'].name
    else:
        configPath = 'None'
        configName = 'None'

    if 'ParameterValuePoint' in request.FILES:
        path = handle_uploaded_file(request.FILES['ParameterValuePoint'])
        r = requests.post(ip + '/admin/toscaValidate', files={'path': open(path, 'rb')})
        obj = r.json()
        if obj['status'] != 'success':
            messages.error(request, 'Invalid (' + request.FILES[
                'ParameterValuePoint'].name + ') file - Not Compliant to TOSCA Standards.')
            return HttpResponseRedirect('/nfv/developer')
        else:
            r = requests.post(ip + '/admin/toscaTranslate', files={'path': open(path, 'rb')})
            obj = r.json()
            parameterValuePointPath = obj['path']
            parameterValuePointName = request.FILES['ParameterValuePoint'].name
    else:
        parameterValuePointPath = 'None'
        parameterValuePointName = 'None'

    dev_api = ip + '/developer/create/'

    #data = {'vnfName':vnfName, 'vnfDesc' : vnfDesc, 'imgLoc' : imgLoc, 'vnfDefinitionName': vnfDefinitionName, 'configName' : configName, 'parameterValuePointName': parameterValuePointName, 'vnfDefinitionPath' : urllib.quote(vnfDefinitionPath, safe=''), 'configPath': urllib.quote(configPath, safe=''), 'parameterValuePointPath' : urllib.quote(parameterValuePointPath, safe=''), 'imagePath' : urllib.quote(imagePath, safe='')}
    data = {'vnfName':vnfName, 'vnfDesc' : vnfDesc, 'imgLoc' : imgLoc, 'vnfDefinitionName': vnfDefinitionName, 'configName' : configName, 'parameterValuePointName': parameterValuePointName, 'vnfDefinitionPath' : vnfDefinitionPath, 'configPath': configPath, 'parameterValuePointPath' : parameterValuePointPath, 'imagePath' : imagePath}
    print '*********************************************************'
    print data
    print '*********************************************************'
    url = dev_api + vnfName + '/' + vnfDesc + '/' + imgLoc + '/' + vnfDefinitionName + '/' + configName + '/' + parameterValuePointName + '/' + urllib.quote(vnfDefinitionPath, safe='') + '/' + urllib.quote(configPath, safe='') + '/' + urllib.quote(parameterValuePointPath, safe='') + '/' + urllib.quote(imagePath, safe='')
    print url
    resp = requests.post(dev_api, json=data)
    item = resp.json()
    if item['CatalogId'] != None:
        print "Success"
        messages.error(request, 'Files Compliant with TOSCA Standards and catalog added successfully with ID:' + item[
            'CatalogId'])
        return HttpResponseRedirect('/nfv/developer')

    return HttpResponseRedirect('/nfv/developer')


def uploadVNF(request):
    ip = 'http://192.168.1.8:8001'
    catalogId = request.POST.get('catalog_id', '')
    print("Upload VNF for catalog:" + catalogId)
    if 'vnfDefinition' in request.FILES:
        path = handle_uploaded_file(request.FILES['vnfDefinition'])
        print ip + '/admin/toscaValidate'
        r = requests.post(ip + '/admin/toscaValidate', files={'path': open(path, 'rb')})
        obj = r.json()
        if obj['status'] != 'success':
            messages.error(request, 'Invalid (' + request.FILES[
                'vnfDefinition'].name + ') file - Not Compliant to TOSCA Standards')
            return HttpResponseRedirect('/nfv/admin')
        else:
            r = requests.post(ip + '/admin/toscaTranslate', files={'path': open(path, 'rb')})
            obj = r.json()
            vnfDefinitionPath = obj['path']
            vnfDefinitionName = request.FILES['vnfDefinition'].name
    else:
        vnfDefinitionPath = 'None'
        vnfDefinitionName = 'None'

    if 'Config' in request.FILES:
        path = handle_uploaded_file(request.FILES['Config'])
        r = requests.post(ip + '/admin/toscaValidate', files={'path': open(path, 'rb')})
        obj = r.json()
        if obj['status'] != 'success':
            messages.error(request,
                           'Invalid (' + request.FILES['Config'].name + ') file - Not Compliant to TOSCA Standards.')
            return HttpResponseRedirect('/nfv/admin')
        else:
            r = requests.post(ip + '/admin/toscaTranslate', files={'path': open(path, 'rb')})
            obj = r.json()
            configPath = obj['path']
            configName = request.FILES['Config'].name
    else:
        configPath = 'None'
        configName = 'None'

    if 'ParameterValuePoint' in request.FILES:
        path = handle_uploaded_file(request.FILES['ParameterValuePoint'])
        r = requests.post(ip + '/admin/toscaValidate', files={'path': open(path, 'rb')})
        obj = r.json()
        if obj['status'] != 'success':
            messages.error(request, 'Invalid (' + request.FILES[
                'ParameterValuePoint'].name + ') file - Not Compliant to TOSCA Standards.')
            return HttpResponseRedirect('/nfv/admin')
        else:
            r = requests.post(ip + '/admin/toscaTranslate', files={'path': open(path, 'rb')})
            obj = r.json()
            parameterValuePointPath = obj['path']
            parameterValuePointName = request.FILES['ParameterValuePoint'].name
    else:
        parameterValuePointPath = 'None'
        parameterValuePointName = 'None'

    dev_api = ip + '/developer/uploadFile/'

    #url = dev_api + catalogId + '/' + vnfDefinitionName + '/' + vnfDefinitionPath.replace('\\',
    #                                                                                      '\\\\') + '/' + configName + '/' + configPath.replace(
    #    '\\', '\\\\') + '/' + parameterValuePointName + '/' + parameterValuePointPath.replace('\\', '\\\\')

    data = {'vnfId':catalogId, 'vnfDefinitionName': vnfDefinitionName, 'configName' : configName, 'parameterValuePointName': parameterValuePointName, 'vnfDefinitionPath' : vnfDefinitionPath, 'configPath': configPath, 'parameterValuePointPath' : parameterValuePointPath}
    print "**************************************************************************"
    #print url
    resp = requests.post(dev_api, json=data)
    item = resp.json()
    messages.error(request, 'Files uploaded successfully')
    return HttpResponseRedirect('/nfv/admin')


def handle_uploaded_file(f):
    print f.name
    extension = f.name.split('.')[-1]
    filename = f.name +`random.random()` + '.' + extension
    path = '/home/rdk/client/' + filename
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path








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
    del request.session['name']
    auth.logout(request)
    return render_to_response('logout.html')

def developer(request):
    #return render_to_response('Developer.html', {'full_name': request.user.first_name})
    if 'name' in request.session:
        return render_to_response('Developer.html',context_instance=RequestContext(request))
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c)

def admin(request):
    #return render_to_response('Admin.html', {'full_name': request.user.first_name})
    if 'name' in request.session:
        return render_to_response('Admin.html', context_instance=RequestContext(request))
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c)

def enterprise(request):
    #return render_to_response('Enterprise.html', {'full_name': request.user.first_name})
    if 'name' in request.session:
        return render_to_response('Enterprise.html', context_instance=RequestContext(request))
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c)





        

