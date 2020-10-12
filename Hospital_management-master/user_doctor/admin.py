from django.contrib import admin
from .models import Appointment,Patient,Doctor,Prescription,doctor_qualification



# Register your models here.  

admin.site.register(Appointment)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(doctor_qualification)
admin.site.register(Prescription)