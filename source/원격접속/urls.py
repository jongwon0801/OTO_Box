# /home/pi/Workspace/newapp/appleapp/urls.py

url(r'^v1/', include('applebox.urls')),

# /home/pi/Workspace/newapp/applebox/urls.py

url(r'^AutosshStart/(?P<outport>[0-9]+)/(?P<inport>\w+)$', views.AutosshStart, name='AutosshStart'),
url(r'^AutosshStop', views.AutosshStop, name='AutosshStop'),
