from django.db import models
from django.db.models import Model 
from django.contrib.auth.models import User 
import datetime

# Create your models here.


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    user_name = models.CharField(max_length=50)
    patient_image = models.ImageField(null = True,blank = True, upload_to = 'patient')
    patient_full_name = models.CharField(null = True, max_length=225)
    patient_dob = models.DateField(null = True)
    patient_blood = models.CharField(null = True, max_length=50)
    patient_mobile = models.CharField(null = True, max_length=225)
    patient_address = models.CharField(null = True, max_length=225)
    patient_city = models.CharField(null = True, max_length=225)
    patient_state = models.CharField(null = True, max_length=225)
    patient_zipcode = models.CharField(null = True, max_length=225)

    @property
    def imageURL(self):
        try:
            url = self.patient_image.url
        except:
            url = ''
        return url        

    

class Doctor(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
   # pres_id = models.ForeignKey(Prescription, on_delete = models.CASCADE, null = True, blank = True)
    doctor_image = models.ImageField(max_length=10000, null = True,blank = True)
    doctor_first_name =models.CharField(max_length=225,null = True)
    doctor_last_name =models.CharField(max_length=225,null = True)
    doctor_email = models.CharField(max_length=225)
    doctor_dob = models.DateField()
    doctor_phone = models.CharField(max_length=225)
    doctor_gender = models.CharField(max_length=50)
    doctor_city = models.CharField(max_length=225)
    doctor_state = models.CharField(max_length=225)
    doctor_zipcode = models.IntegerField()
    doctor_services = models.CharField(max_length=225)
    doctor_Field = models.CharField(max_length=225)

    @property
    def imageURL(self):
        try:
            url = self.doctor_image.url
        except:
            url = ''
        return url  


class doctor_qualification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, null = True, blank = True)
    doctor_degree = models.CharField(max_length=225)
    doctor_college = models.CharField(max_length=225)
    doctor_year = models.CharField(max_length=225)

    




class Appointment(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    patient_id = models.ForeignKey(Patient, on_delete = models.CASCADE, null = True, blank = True)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, null = True, blank = True)
    time_field = models.CharField(max_length=50,null=True)
    date_field = models.DateField(null=True) 
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(null=True)
    

   



class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE, null = True, blank = True)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, null = True, blank = True)
    appointment = models.ForeignKey(Appointment, on_delete = models.CASCADE, null = True, blank = True)
    medicine = models.CharField(max_length=2500, null=True)
 


    


  


