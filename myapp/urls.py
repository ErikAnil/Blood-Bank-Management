from django.urls import path
from . import views
urlpatterns=[
    path('',views.index),
    path('h/',views.index),
    path('dr/',views.donerreg),
    #path('pr/',views.patientreg),
    path('pr/', views.patient_registration, name='patient_registration'),

    path('abt/',views.adminbloodtransfer),
    path('tr/<int:id>/', views.admintransfer),
    path('astk/',views.adminstock),




    path('abdt/', views.adminblooddirecttransfer),
    path('adtrs/<int:id>/',views.admindirecttrans),
    path('reject/<int:id>/', views.reject_request, name='reject_request'),

    path('ap/',views.adminpage),
    path('adapr/',views.admindonerapproval),
    path('aad/<int:id>/',views.approvedoner),
    path('amr/<int:id>/', views.rejectdoner),
    path('dap/<int:id>/accept/', views.donerpatientapp, name='accept_donor'),


    path('vadh/<int:id>/',views.adminviewhistory),
    path('anoti/',views.adminnotification),
    path('chp/',views.changepass),



    path('pp/',views.patientpage),
    path('pbk/<int:id>/',views.patientrequest),
    path('pvsts/',views.userviewstatus),
    path('pfback/',views.patientfeedback),
    path('pfb/<int:did>/',views.patientfeedback1),
    path('uvnot/',views.patientnotification),
    path('dbk/',views.patientdirectrequest),
    path('ajax/load-options/', views.load_options, name='ajax_load_options'),


    path('dp/',views.donerpage),
    path('dpa/',views.donerpatientapproval),
    path('dap/<int:id>/',views.donerpatientapp),
    path('drj/<int:id>/',views.donerpatientreject),
    path('vdh/',views.viewdonerhistory),
    path('vdnot/',views.viewdonernotification),
    path('vdof/',views.viewdonerfeedback),

    path('log/',views.loginpage),
    path('delnot/<int:id>/',views.delnotification),

]