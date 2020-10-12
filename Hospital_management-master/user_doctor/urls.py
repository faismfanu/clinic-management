from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
 
 #-----------------------------patient_views--------------------------------------------------#

    path('',views.index,name="index"),
    path('login',views.login,name="login"),
    path('guestlogin/<int:id>',views.guest_login,name="guestlogin"),
    path('signup',views.signup,name="signup"),
    path('useraccount',views.user_account,name="user_account"),
    path('patient_prescription/<int:id>/<int:doc_id>',views.patient_result,name='patient_prescription'),
    path('patient_profile',views.patient_profile,name="patient_profile"),
    path('booking/<int:id>',views.booking,name="booking"),
    path('bookingsave/<int:id>',views.booking_save,name="booking_save"),
    path('bookingsuccess',views.booking_success,name="booking_success"),
    path('cancel_booking/<int:id>',views.cancel_booking,name="cancel_booking"),
    path('logout',views.logout,name="logout"),
    path('mobail/',views.mobail,name="mobail"),
    path('otp/',views.otp,name="otp"),
    
    
#-------------------------------doctor_login----------------------------------------------------#    
    
    path('doctorlogin',views.doctorlogin,name="doctorlogin"),
    path('doctorappointment',views.doctor_appointment,name="doctor_appointment"),
    path('doctorprescription/<str:id>/<int:appointment_id>',views.doctor_priscription,name="doctor_priscription"),
    path('savemedicine/<int:id>/<int:time_id>',views.save_medicine, name = 'save_medicine'),
    path('doctorbooking',views.doctor_booking,name="doctor_booking"),
    path('edit_doctor/<int:id>/<int:user_id>',views.edit_doctor,name= 'edit_doctor'),
    path('doctorpatients',views.doctor_patients,name="doctor_patient"),
    path('doctorprofile/<int:id>',views.doctor_profile,name="doctor_profile"),
    path('doctor_patient_profile/<int:id>',views.doctor_patient_profile,name="doctor_patient_profile"),
    path('patientsample',views.patientsample,name="patientsample"),


    


#----------------------------`----admin_login----------------------------------------------------#
    
    path('admin',views.admin_login,name='admin_login'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('adminpanel',views.adminpanel,name='adminpanel'),
    path('adminadddoctor',views.admin_add_doctor,name='adminadddoctor'),
    path('update_doctor/<int:id>/<int:user_id>',views.update_doctor,name='update_doctor'),
    path('delete_doctor/<int:id>',views.delete_doctor,name='delete_doctor'),
    path('sample',views.sample,name='sample'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)