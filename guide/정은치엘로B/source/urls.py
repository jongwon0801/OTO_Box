"""appleapp URL Configuration
# /home/pi/Workspace/appleapp/appleapp/urls.py


The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
urlpatterns = [
    url(r'^logsKivy$', views.LogsKivy, name='LogsKivy'),
    url(r'^logsKivy/(?P<filename>[-\w.]+)/$', views.LogsKivyFile, name='LogsKivyFile'),
    url(r'logsDjango$', views.LogsDjango, name='LogsDjango'),
    url(r'logsDjango/(?P<filename>[-\w.]+)/$', views.LogsDjangoFile, name='LogsDjangoFile'),
    url(r'^logsPush', views.LogsPush, name='LogsPush'),
    url(r'^$', views.index,name='index'),
    url(r'^whois', views.whois, name='whois'),
    url(r'^admin/', admin.site.urls),
    url(r'^v1/', include('applebox.urls')),
    url(r'^readme/', views.readme, name='readme'),
    url(r'^setup/', views.setup, name='setup'),
    url(r'^test/', views.test, name='test'),
    url(r'^o2obox', views.api, name='api'),
    url(r'^django/', views.django, name='django'),
    url(r'^newinstall/', views.newinstall, name='newinstall'),
    url(r'^raspberrypi/', views.raspberrypi, name='raspberrypi'),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
