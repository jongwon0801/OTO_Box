# /home/pi/Workspace/newapp/applebox/urls.py

from django.conf.urls import url
from django.urls import re_path
from . import views
from django.conf.urls import handler404
from django.conf.urls import handler500
app_name = 'applebox'


urlpatterns = [
    #url(r'^$', views.index, name='index'),
    #url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    #url(r'^AppleboxAll/(?P<yid>[0-9]+)/$', views.AppleboxAll, name='vote'),
    url(r'^Config/(?P<osname>\w+)/(?P<appversion>[0-9]+)$', views.Config, name='Config'),
    url(r'^AppleboxAll/(?P<yid>[0-9]+)$', views.AppleboxAll, name='AppleboxAll'),
    url(r'^Status/(?P<yid>[0-9]+)$', views.Status, name='Status'),
    url(r'^Sensor/(?P<yid>[0-9]+)$', views.Sensor, name='Sensor'),
    url(r'^StatusLocker/(?P<yid>[0-9]+)$', views.StatusLocker, name='StatusLocker'),
    url(r'^StatusServer/(?P<yid>[0-9]+)$', views.StatusServer, name='StatusServer'),
    url(r'^StatusReverse/(?P<yid>[0-9]+)$', views.StatusReverse, name='StatusReverse'),
    url(r'^Applebox/(?P<yid>[0-9]+)$', views.Applebox1, name='Applebox1'),
    url(r'^Locker/(?P<yid>[0-9]+)$', views.LockerList, name='Locker'),
    url(r'^LockerUpdate/(?P<yid>[0-9]+)$', views.LockerUpdate, name='LockerUpdate'),
    url(r'^OpenToSave/(?P<yid>[0-9]+)$', views.OpenToSave, name='OpenToSave'),
    url(r'^OpenToSaveAll/(?P<yid>[0-9]+)$', views.OpenToSaveAll, name='OpenToSaveAll'),
    url(r'^OpenToTake/(?P<yid>[0-9]+)$', views.OpenToTake, name='OpenToTake'),
    url(r'^OpenToAdmin/(?P<yid>[0-9]+)$', views.OpenToAdmin, name='OpenToAdmin'),
    url(r'^SensorStart/(?P<yid>[0-9]+)$', views.SensorStart, name='SensorStart'),
    url(r'^SensorStop/(?P<yid>[0-9]+)$', views.SensorStop, name='SensorStop'),
    url(r'^OpenToTakeAll/(?P<yid>[0-9]+)/(?P<acceptNumber>[0-9]+)$', views.OpenToTakeAll, name='OpenToTakeAll'),
    url(r'^Rfid/(?P<tagid>\w+)$', views.GetRfid, name='GetRfid'),
    url(r'^Rfid$', views.RfidList, name='RfidList'),
    url(r'^RfidChange/(?P<dong>\w+)/(?P<ho>\w+)$', views.RfidChange, name='RfidChange'),
    url(r'^Pincode/(?P<yid>[0-9]+)/(?P<pincode>\w+)$', views.GetPincode, name='GetPincode'),
    url(r'^SmsAuth/(?P<yid>[0-9]+)/(?P<hp>\w+)$', views.SmsAuth, name='SmsAuth'),
    url(r'^RfidReg/(?P<yid>[0-9]+)$', views.RfidReg, name='RfidReg'),
    url(r'^RfidSync/(?P<yid>[0-9]+)$', views.RfidSync, name='RfidSync'),
    url(r'^MyBox/(?P<yid>[0-9]+)$', views.MyBox, name='MyBox'),
    url(r'^AcceptNumber/(?P<yid>[0-9]+)/(?P<acceptNumber>[0-9]+)/(?P<status>[.\w]+)/(?P<usage>[.\w]+)$', views.AcceptNumber, name='AcceptNumber'),

    url(r'^MyLocker/(?P<dong>\w+)/(?P<ho>\w+)$', views.MyLocker, name='MyLocker'),
    url(r'^TakeLog/(?P<yid>[0-9]+)$', views.TakeLogList, name='TakeLogList'),
    url(r'^PushList/(?P<yid>[0-9]+)$', views.PushList, name='PushList'),
    url(r'^PushDelete/(?P<yid>[0-9]+)$', views.PushDelete, name='PushDelete'),
    url(r'^SaveLog/(?P<yid>[0-9]+)$', views.SaveLogList, name='SaveLogList'),
    url(r'^House/(?P<dong>\w+)$', views.DongList, name='DongList'),
    #url(r'^House/(?P<dong>\w+)$', views.HoList, name='HoList'),
    url(r'^House/(?P<dong>\w+)/(?P<ho>\w+)$', views.HouseSelect, name='HouseSelect'),
    url(r'^PasswordChange/(?P<dong>\w+)/(?P<ho>\w+)$', views.PasswordChange, name='PasswordChange'),
    #url(r'^Resident', views.ResidentList, name='ResidentList'),
    #url(r'^Resident', views.ResidentList, name='ResidentList'),


    url(r'^Install/(?P<yid>[0-9]+)$', views.Install, name='Install'),
    #url(r'^Network/(?P<yid>[0-9]+)/(?P<buyerSq>[0-9]+)$', views.Install, name='Install'),
    url(r'^House$', views.HouseReq, name='HouseReq'),
    url(r'^Notice$', views.NoticeList, name='NoticeList'),
    url(r'^PropertyList$', views.PropertyList, name='PropertyListList'),
    url(r'^Property$', views.PropertyReq, name='PropertyReq'),
    url(r'^Property/(?P<name>\w+)$', views.PropertyItemReq, name='PropertyItemReq'),
    url(r'^Resident$', views.ResidentReq, name='ResidentReq'),
    url(r'^Resident/(?P<tagid>\w+)$', views.GetResident, name='GetResident'),
    url(r'^ResidentUpdate/(?P<dong>\w+)/(?P<ho>\w+)$', views.ResidentUpdate, name='ResidentUpdate'),
    url(r'^Processes$', views.ProcessList, name='ProcessList'),
    url(r'^ExecuteProcess$', views.ExecuteProcess, name='ExecuteProcess'),
    url(r'^MakePassword/(?P<yid>[0-9]+)$', views.MakePassword, name='MakePassword'),

    #url(r'^Property/(?P<name>\w+)$', views.PropertyItemReq, name='PropertyItemReq'),

    url(r'^LockerSync/(?P<yid>[0-9]+)$', views.LockerSync, name='LockerSync'),
    url(r'^NoticeSync$', views.NoticeSync, name='NoticeSync'),
    url(r'^AutosshStart/(?P<outport>[0-9]+)/(?P<inport>\w+)$', views.AutosshStart, name='AutosshStart'),
    url(r'^AutosshStop', views.AutosshStop, name='AutosshStop'),
    url(r'^Cmd', views.Cmd, name='Cmd'),
    url(r'^SignIn', views.SignIn, name='SignIn'),
    url(r'^SignOut', views.SignOut, name='SignOut'),
    url(r'^CodeTbl/(?P<gCode>[.\w]+)$', views.CodeTbls, name='CodeTbls'),
    url(r'^Reset$', views.Reset, name='Reset'),
    url(r'^NetworkCheck$', views.NetworkCheck, name='NetworkCheck'),

    url(r'^NetworkChange$', views.NetworkChange, name='NetworkChange'),
    url(r'^Network$', views.NetworkInfo, name='NetworkInfo'),
    url(r'^Service/(?P<yid>[0-9]+)$', views.ServiceList, name='ServiceList'),
    url(r'^Reserve/(?P<yid>[0-9]+)/(?P<status>[.\w]+)$', views.Reserve, name='Reserve'),
    #url(r'^ReserveConfirm/(?P<yid>[0-9]+)$', views.ReserveConfirm, name='ReserveConfirm'),

    url(r'^TestOpenAll$', views.TestOpenAll, name='TestOpenAll'),
    url(r'^PrintReceipt$', views.PrintReceipt, name='PrintReceipt'),
    url(r'^ParcelPost$', views.ParcelPost, name='ParcelPost'),


    url(r'^Locker/close_to_save_all$', views.close_to_save_all, name='close_to_save_all'),
    url(r'^Locker/open_to_save$', views.open_to_save, name='open_to_save'),
    url(r'^Locker/close_to_save$', views.close_to_save, name='close_to_save'),
    url(r'^Locker/open_to_take$', views.open_to_take, name='open_to_take'),
    url(r'^Locker/open_to_take_all$', views.open_to_take_all, name='open_to_take_all'),
    url(r'^Locker/close_to_take$', views.close_to_take, name='close_to_take'),
    url(r'^Smses$', views.SmsList, name='SmsList'),
    url(r'^BizMsg$', views.SmsInsert, name='SmsInsert'),
    #url(r'^OrderTemp$', views.OrderTemp, name='OrderTemp'),
]
#handler500 = views.error500
#handler500 = 'applebox.views.error500'
