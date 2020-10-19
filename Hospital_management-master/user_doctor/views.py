from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .models import Appointment, Patient, Prescription, Doctor,doctor_qualification,Doctor_patient,Blocked_users    
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib import messages
from datetime import date
import datetime
import requests
import json
from django.db.models import DateTimeField
from django.db.models.functions import Trunc
import base64
from PIL import Image
from base64 import decodestring
import binascii
from django.core.files import File
from django.http import JsonResponse 
from django.core.files.base import ContentFile


# Create your views here.

def index(request):
   doctors = Doctor.objects.all()
   return render(request, 'index.html', {'doctors': doctors})


def login(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff == 1:
                auth.login(request, user)
                return redirect('/')
                #if user.is_staff == 1:
                    #return redirect('/')
            else:
                messages.error(request, 'Invalid username and password')
                return redirect('login')

        else:
            messages.error(request, 'Invalid username and password')
            return redirect('login')
    else:
        return render(request, 'login.html')


def signup(request):
    patients = Patient()
    if request.method == 'POST':
        username = request.POST['username']
        number = request.POST['number']
        password = request.POST['password']
        password1 = request.POST['password2']
        dicti = {"username": username}
        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already taken', dicti)
                return render(request, 'signup.html', dicti)
            elif User.objects.filter(last_name=number).exists():
                messages.info(request, 'mobile number already exist', dicti)
                return render(request, 'signup.html', dicti)    
            else:
              user = User.objects.create_user(
              username=username,  password=password, last_name=number, first_name=password, is_staff=1)
              patients.user = user
              patients.user_name = request.POST.get('username')
              patients.patient_full_name = request.POST.get('patient_full_name')
              patients.patient_mobile = request.POST.get('number')
              patients.save()
              user.save()
              number = request.POST['number']
              user=User.objects.get(last_name=number)
              print(user)
              if user:
                  username = user.username
                  password=user.first_name
                  request.session['username'] =  username
                  request.session['password'] = password
                

                  url = "https://d7networks.com/api/verifier/send"
                  number=str(91) + number
                    
                  payload = {'mobile': number,
                  'sender_id': 'SMSINFO',
                  'message': 'Your otp code is {code}',
                  'expiry': '900'}
                  files = [

                  ]
                  headers = {
                  'Authorization': 'Token 40fb19ebcd55aeba923ef6c03191ef6857cda031'
                   }

                  response = requests.request("POST", url, headers=headers, data = payload, files = files)

                  print(response.text.encode('utf8'))
                  data=response.text.encode('utf8')
                  datadict=json.loads(data.decode('utf-8'))

                  id=datadict['otp_id']
                  status=datadict['status']
                  print('id:',id)
                  request.session['id'] = id
                
                  return render(request,'otp.html')

              else:
                  messages.info(request,'mobail number not registerd')
                  return redirect('signup')

        else:
            messages.info(request,"Password doesn't match")
            return render(request,'signup.html')
              
    return render(request, 'signup.html')          


def guest_login(request,id):
     doctor=Doctor()
     doctor = Doctor.objects.get(id=id)
     if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            if user.is_staff == 1:
                auth.login(request, user)
                return redirect('booking',id=doctor.id)
            else:
                messages.error(request, 'Invalid username and password')
                return render(request, 'guest_login.html', {'doctor':doctor})

        else:
            messages.error(request, 'Invalid username and password')
            return render(request, 'guest_login.html', {'doctor':doctor})
     else:
        return render(request, 'guest_login.html', {'doctor':doctor})

   


def mobail(request):
    if request.method=='POST':
        number = request.POST['number']
        user=User.objects.get(last_name=number)
        print(user)
        if user:
            username = user.username
            password=user.first_name
            request.session['username'] =  username
            request.session['password'] = password
        

            url = "https://d7networks.com/api/verifier/send"
            number=str(91) + number
            
            payload = {'mobile': number,
            'sender_id': 'SMSINFO',
            'message': 'Your otp code is {code}',
            'expiry': '900'}
            files = [

            ]
            headers = {
            'Authorization': 'Token 40fb19ebcd55aeba923ef6c03191ef6857cda031'
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)

            print(response.text.encode('utf8'))
            data=response.text.encode('utf8')
            datadict=json.loads(data.decode('utf-8'))

            id=datadict['otp_id']
            status=datadict['status']
            print('id:',id)
            request.session['id'] = id
           
            return render(request,'otp.html')

        else:
            messages.info(request,'mobail number not registerd')
            return render(request,'mobail.html')        
    return render(request,'mobail.html')


def otp(request):
    if request.method=='POST':
        otp=request.POST['otp']
       
        id=request.session['id']
        url = "https://d7networks.com/api/verifier/verify"

        payload = {'otp_id': id,
        'otp_code': otp}
        files = [

        ]
        headers = {
        'Authorization': 'Token 40fb19ebcd55aeba923ef6c03191ef6857cda031'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)

        print(response.text.encode('utf8'))
        data=response.text.encode('utf8')
        datadict=json.loads(data.decode('utf-8'))
        status=datadict['status']

        if status=='success':
            username = request.session['username']   
            password =  request.session['password']
            per=authenticate(username=username,password=password)
            auth.login(request,per)
            return redirect(index)
        
        else:
            messages.info(request,'incorrectotp')
            return render(request,'otp.html')

    return render(request,'otp.html')


@staff_member_required(login_url='/')
def user_account(request):
    patient = request.user.patient
    patient_id = request.user.id
    patients = Patient.objects.get(user=patient_id)
    prescription = Prescription.objects.filter(patient_id=patient)
    print(patient)
    times =  Appointment.objects.filter(patient_id=patient).order_by('-id')
    print(times)
    return render(request, 'user_account.html', {'times':times,'prescription':prescription,'patients':patients})



@staff_member_required(login_url='/')
def patient_result(request,id,doc_id):
    doctor=Doctor()
    doctor = Doctor.objects.get(id=doc_id)
    print(doctor)
    prescription = Prescription.objects.get(appointment=id)
    print(prescription)
    patient = request.user.patient
    print(patient)
    times =  Appointment.objects.filter(patient_id=patient)
    print(times)
    return render(request, 'patient_result.html', {'times':times ,'doctor':doctor, 'prescription':prescription})    


@staff_member_required(login_url='/')
def patient_profile(request):
    patient = Patient()
    user = request.user.id
    print(user)
    user = User.objects.get(id=user)
    patient = Patient.objects.get(user=user)
    print(patient)
   # patient = Patient.objects.get(id=id)
    if request.method == 'POST':
        email = request.POST['email']
        user.email=email
        user.save()
        patient.patient_full_name = request.POST.get('patient_full_name')
        patient.patient_dob = request.POST.get('patient_dob')
        patient.patient_mobile = request.POST.get('patient_mobile')
        patient.patient_blood = request.POST.get('patient_blood')
        patient.patient_city = request.POST.get('patient_city')
        patient.patient_state = request.POST.get('patient_state')
        patient.patient_zipcode = request.POST.get('patient_zipcode')
        patient.patient_address = request.POST.get('patient_address')
        image_data =request.POST.get('image64data')
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr),name= str(user.id)+'.' +ext)
        try:
            patient.patient_image = data
        except:
            patient.patient_image = 0
        patient.save()
        return redirect('patient_profile')

    else:
        return render(request, 'edit_patient_profile.html',{"patient":patient})



@staff_member_required(login_url='/')
def booking(request,id):
    doctor=Doctor()
    user = request.user.id
    patient = Patient.objects.get(user=user)
    print("blah",patient)
    doctor = Doctor.objects.get(id=id)
    try:
        block_user = Blocked_users.objects.get(patient=patient,doctor=id)
    except:
        block_user = 0    
    print('soha',block_user)

    return render(request, 'booking.html',{'doctor':doctor,'block_user':block_user})    



@staff_member_required(login_url='/')
def booking_save(request,id):
     if request.method =='POST':
        times =  Appointment()
        doctor = Doctor()
        patient_name = request.user
        patient_user = request.user.id
        print(patient_user)
        #times.patient = request.user.patient
        patient = Patient.objects.get(user=patient_user)
        print(patient) 
        doctor = Doctor.objects.get(id=id)
        print(doctor)
        doctor_patient, created = Doctor_patient.objects.get_or_create(doctor=doctor, patient=patient)
        times.patient_id = patient 
        times.doctor = doctor
        times.user_id = patient_name
        times.date_field = request.POST.get('txtDate')
        times.time_field = request.POST.get('course')
        times.status = 0
        times.save()
        return redirect('booking_success')
     else:
        return render(request,'booking.html')


@staff_member_required(login_url='/')
def booking_success(request):
    return render(request, 'booking_success.html')   


@staff_member_required(login_url='/')
def cancel_booking(request,id):
    #times = Appointment()
    times = Appointment.objects.get(id=id)
    times.status = 1
    print('status:',times.status )
    times.save()       
    return redirect('user_account')



def logout(request):
    auth.logout(request)
    return redirect('/')
 
#-----------------------------------doctor_view-------------------------------------------------#

def doctorlogin(request):
     if request.user.is_authenticated:
        return redirect('doctor_appointment')
     if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff == 0:
                auth.login(request,user)
                if user.is_staff == 0:
                    return redirect('doctor_appointment')
            else:
                messages.error(request, 'Invalid username and password')
                return redirect('doctorlogin')

        else:
            messages.error(request, 'Invalid username and password')
            return redirect('doctorlogin')
     else:
         return render(request,'doctor_login.html')


    # if request.method == "POST":
    #     u_name = request.POST.get('username')
    #     p_word = request.POST.get('password')
    #     if u_name == "doctor" and p_word == "123456":
    #         return redirect("doctor_appointment")
    #     return render(request,'doctor_login.html')
    # else:
    #      return render(request, 'doctor_login.html')
    # return render(request, 'doctor_login.html')     


def doctor_profile(request,id):
    doctor=Doctor()
    doctor = Doctor.objects.get(id=id)
    return render(request, 'doctor_profile.html',{'doctor':doctor})

@login_required(login_url='doctorlogin')
def doctor_patient_profile(request,id):
    user = User.objects.get(id=id)
    times = Appointment.objects.filter(user_id=id)
    print(times)
    return render(request, 'doctor_patient_profile.html',{'user':user,'times':times})


@login_required(login_url='doctorlogin')
def doctor_appointment(request):
    doctor = Doctor()
    doctor_user = request.user.id
    print(doctor_user)
    doctor, created = Doctor.objects.get_or_create(user_id = doctor_user)
    #user = User.objects.get(id=patient)
    print(doctor.id)
    #doctor = Doctor.objects.get(id=16)
    times =  Appointment.objects.filter(doctor_id=doctor.id).order_by('-id')
    print(times)

    today = date.today()
    return render(request, 'doctor_appointment.html', {'times':times,'today':today,'doctor':doctor})


# def doctor_profile_settings(request):
#     return render(request, 'doctor_profile_settings.html    ')

@login_required(login_url='doctorlogin')
def doctor_priscription(request,id,appointment_id):
    patient = Patient.objects.get(id=id)
    times = Appointment.objects.get(id=appointment_id)
    # times.status = 2
    # print('status:',times.status )
    times.save()       
    return render(request, 'doctor_priscription.html',{'patient':patient,'times':times})

@login_required(login_url='doctorlogin')
def save_medicine(request,id,time_id):
    if request.method == 'POST':
        doctor = Doctor()
        time = Appointment.objects.get(id=time_id)
        doctor_user = request.user.id
        patient = Patient.objects.get(id=id)
        print(patient)
        doctor, created = Doctor.objects.get_or_create(user_id = doctor_user)
        print(doctor_user)
        medicines = Prescription()
        medicines.patient = patient
        medicines.doctor = doctor
        medicines.appointment = time
        medicines.medicine = request.POST.get('textfield')
        #medicines.status = 0
        time.status = 2
        time.save()
        medicines.save()
        return redirect('doctor_appointment')
    else:
        return render(request, 'doctor_priscription.html')    

@login_required(login_url='doctorlogin')
def edit_doctor(request,id,user_id):
    doctors =Doctor()
    user = User()
    doctors = Doctor.objects.get(id=id)
    user = User.objects.get(id=user_id)
    print(user)
    if request.method == 'POST':  
        first_name = request.POST['doctor_first_name']
        last_name = request.POST['doctor_last_name']
        email = request.POST['email']
        user.first_name = first_name
        user.last_name = last_name
        user.email=email
        user.save()
        doctors.doctor_first_name = request.POST.get('doctor_first_name')
        doctors.doctor_last_name = request.POST.get('doctor_last_name')
        doctors.doctor_email = request.POST.get('email')
        doctors.doctor_dob = request.POST.get('doctor_dob')
        doctors.doctor_phone = request.POST.get('doctor_phone')
        doctors.doctor_gender = request.POST.get('doctor_gender')
        doctors.doctor_city = request.POST.get('doctor_city')
        doctors.doctor_state = request.POST.get('doctor_state')
        doctors.doctor_zipcode = request.POST.get('doctor_zipcode')
        doctors.doctor_services = request.POST.get('services')
        doctors.doctor_qualification = request.POST.get('qualification')
        doctors.doctor_Field = request.POST.get('Field')
        image_data =request.POST.get('image64data')
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr),name= str(user.id)+'.' +ext)
        doctors.doctor_image = data
        doctors.save()
        return redirect('doctor_appointment')
    return render(request, 'edit_doctor.html' ,{'doctors':doctors,'user':user}) 




def doctor_booking(request):
    return render(request, 'doctor_booking.html')  


@login_required(login_url='doctorlogin')
def doctor_patients(request):
    doctor = Doctor()
    # doctor = Doctor.objects.get(id=id)
    user = request.user.id
    print(user)
    user = User.objects.filter(is_superuser= False, is_staff=1)
    return render(request, 'doctor_patients.html', {'user':user,'doctor':doctor})      

@login_required(login_url='doctorlogin')
def patientsample(request):
    doctor = Doctor()
    time = Appointment()
    user = request.user.id
    doctor = Doctor.objects.get(user_id=user)
    try:
        doctor_q = doctor_qualification.objects.get(doctor=doctor)
    except:
        doctor_q = 0  
    print(user)
    doctor_patient = doctor.doctor_patient_set.all()
    print('ggggg',doctor_patient)
    patient = Patient()
    patient = Patient.objects.all()
    time = Appointment.objects.all()
    print(patient)
    return render(request, 'patientsample.html',{'patient':patient,'doctor':doctor,'time':time,'doctor_q':doctor_q,'doctor_patient':doctor_patient})   


@login_required(login_url='doctorlogin')
def patient_profile_sample(request,id,pat_id,doc_id):
    patient = Patient.objects.get(id=pat_id)
    doctor = Doctor.objects.get(id=doc_id)
    print(doctor)
    times = Appointment.objects.filter(user_id=id,doctor=doc_id)
    try:
        block_user = Blocked_users.objects.get(patient=pat_id,doctor=doc_id)
    except:
        block_user = 0

    print('bbbb',block_user)
    print(times)
    return render(request, "patient_profile_sample.html",{"patient":patient,'times':times,'doctor':doctor,'block_user':block_user})

@login_required(login_url='doctorlogin')
def block_user(request,pat_id,doc_id):
    doctor = Doctor()
    patient = Patient()
    block_user = Blocked_users()
    doctor = Doctor.objects.get(id=doc_id)
    print(doctor)
    patient = Patient.objects.get(id=pat_id)
    print(patient)
    block_user, created = Blocked_users.objects.get_or_create(doctor=doctor, patient=patient,status=0)
    return redirect('patient_profile_sample', patient.user.id , patient.id,doctor.id)

@login_required(login_url='doctorlogin')
def unblock_user(request,id,pat_id,doc_id):
    doctor = Doctor()
    patient = Patient()
    doctor = Doctor.objects.get(id=doc_id)
    print(doctor)
    patient = Patient.objects.get(id=pat_id)
    block_user = Blocked_users.objects.get(id=id)
    print('uuu0',block_user)
    block_user.delete()
    return redirect('patient_profile_sample', patient.user.id , patient.id ,doctor.id) 


#----------------------------------Admin_view--------------------------------------------#

def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
            return redirect("adminpanel")
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
          if username == 'ganesh' and password == '123456':
              auth.login(request, user)
              return redirect('adminpanel')
        else:
             messages.info(request, "Invalid username and password.")
             return HttpResponseRedirect(request.path_info)  
    return render(request, "admin_login.html")

def admin_logout(request):
    auth.logout(request)
    return redirect('admin_login')


@user_passes_test(lambda u: u.is_superuser)
def adminpanel(request):
    user = User.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'admindoctor.html',{'doctors':doctors})

@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def admin_add_doctor(request):
    if request.method == 'POST':
        doctors = Doctor()
        user = request.user
        qualification = doctor_qualification.objects.create(doctor=doctors.id)
        username = request.POST['doctor_user_name']
        first_name = request.POST['doctor_first_name']
        last_name = request.POST['doctor_last_name']
        email = request.POST['doctor_email']
        password = request.POST['doctor_password'] 
        if User.objects.filter(username=username).exists():
            messages.info(request, 'username already taken')
            return render(request, 'adminadddoctor.html')
        elif User.objects.filter(email=email).exists():
                messages.info(request, 'email already taken')
                return render(request, 'adminadddoctor.html')
        else:
            user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name,is_staff=0)
            doctors.user_id = user
            doctors.doctor_first_name = request.POST.get('doctor_first_name')
            doctors.doctor_last_name= request.POST.get('doctor_last_name')
            # doctors.doctor_password = request.POST.get('doctor_password')
            doctors.doctor_email = request.POST.get('doctor_email')
            doctors.doctor_dob = request.POST.get('doctor_dob')
            doctors.doctor_phone = request.POST.get('doctor_phone')
            doctors.doctor_gender = request.POST.get('doctor_gender')
            doctors.doctor_city = request.POST.get('doctor_city')
            doctors.doctor_state = request.POST.get('doctor_state')
            doctors.doctor_zipcode = request.POST.get('doctor_zipcode')
            doctors.doctor_services = request.POST.get('services') 
            doctors.doctor_Field = request.POST.get('Field')
            image_data =request.POST.get('image64data')
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),name= str(user.id)+'.' +ext)
            doctors.doctor_image = data
            user.save()
            doctors.save()
            messages.error(request,"New Doctor Added")
            return redirect('adminpanel')
    else:
        return render(request, 'adminadddoctor.html')    


@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def update_doctor(request,id,user_id):
    doctors =Doctor()
    doctors = Doctor.objects.get(id=id)
    user = User.objects.get(id=user_id)
    print(user)
    if request.method == 'POST':
        first_name = request.POST['doctor_first_name']
        last_name = request.POST['doctor_last_name']
        email = request.POST['email']
        user.first_name = first_name
        user.last_name = last_name
        user.email=email
        user.save()
        doctors.doctor_name = request.POST.get('username')
        doctors.doctor_email = request.POST.get('email')
        doctors.doctor_dob = request.POST.get('doctor_dob')
        doctors.doctor_phone = request.POST.get('doctor_phone')
        doctors.doctor_gender = request.POST.get('doctor_gender')
        doctors.doctor_city = request.POST.get('doctor_city')
        doctors.doctor_state = request.POST.get('doctor_state')
        doctors.doctor_zipcode = request.POST.get('doctor_zipcode')
        doctors.doctor_services = request.POST.get('services')
        doctors.doctor_qualification = request.POST.get('qualification')
        doctors.doctor_Field = request.POST.get('Field')
        image_data =request.POST.get('image64data')
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr),name= str(user.id)+'.' +ext)
        doctors.doctor_image = data                
        # if 'myfile' not in request.POST: 
        # else:
        #      doc = Doctor.objects.get(id=id)
        #      doctors.doctor_image = doc.doctor_image
        doctors.save()
        return redirect('adminpanel')

    return render(request, 'update_doctor.html' ,{'doctors':doctors,'user':user})     


@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def delete_doctor(request,id,user_id):
    doctor =Doctor()
    user = User.objects.get(id=user_id)
    print(user)
    doctor = Doctor.objects.get(id=id)
    print(doctor)
    user.delete()
    doctor.delete()
    return redirect('adminpanel')



def sample(request):
    return render(request, 'sample.html')


def addmove(request):
    text = request.POST.getlist('det_ails[]')
    for texts in text:
        print(texts)
    return redirect('/')



 # doc = request.POST.get('docname')  
    # print('kooi',doc)  
    # dl = request.POST.get('dl')
    # # print(dl)
    # user = User.objects.get(username=dl)
    # doc = Doctor.objects.get(user_id=user)



    # print("adsfdasf",doc) 
    
    
    #     colifi = doctor_qualification.objects.create(doctor_degree=texts,doctor=doc)
    # return JsonResponse({'xc':2},status=200)    