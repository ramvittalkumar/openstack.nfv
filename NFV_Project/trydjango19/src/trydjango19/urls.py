"""trydjango19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.conf.urls.static import static
from nfv import views

# from . import views {
# {
#    login,
#    auth_view,
#    Developer,
# }


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^nfv/$', "nfv.views.login"),
     url(r'^nfv/login/$', "nfv.views.login"),
    #url(r'^nfv/submit/$', "nfv.views.submit"),
    url(r'^nfv/auth/$', "nfv.views.auth_view"),
    url(r'^nfv/invalid/$', "nfv.views.invalid_login"),
    url(r'^nfv/logout/$', "nfv.views.logout"),
    url(r'^nfv/developer/$', "nfv.views.developer"),
    url(r'^nfv/admin/$', "nfv.views.admin"),
    url(r'^nfv/enterprise/$', "nfv.views.enterprise"),
    url(r'^$', "nfv.views.auth_view"),
 #   url(r'^nfv/$', "login"),
 #   url(r'^auth/$', "auth_view"),
 #   url(r'^developer/$', "Developer"),
    #url(r'^nfv/$', "nfv.views.Admin"),
    #url(r'^nfv/$', "nfv.views.Enterprise"),
    
]

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
