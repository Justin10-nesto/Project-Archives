from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth.models import User,auth,Permission,Group
from django.contrib import messages
from django.db.models import Q
from .models import *
from django.contrib.auth.hashers import make_password
import random 
import os
import datetime
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.template import defaultfilters
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import formats
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
import math
from django.contrib.auth.decorators import *
from email.mime.image import MIMEImage
from RaphaelSomaDIT import rex
from django.core.files import File
from .models import *



def  login(request):
   user = User()
   students = Student()
   staffs = Staff()
   
   if request.method == 'POST':
      email=request.POST.get("username")
      password=request.POST.get("password")
      users = User.objects.filter(username=email).exists()
      u = User.objects.filter(username=email)
      
      u = user.first_name.split(',')
      u = u
      
      current_date = datetime.datetime.now().date()
      october = datetime.datetime(current_date.year,10,1).date()
      
   
      if users:
         if current_date >=october:
            rex.studentInfo(email=request.POST.get("username"), password=request.POST.get("password"))
            if rex.error == "no internet connection":
               print(rex.error)
               return HttpResponse('no connection')
            elif rex.error == "Login Failed: invalid credentials":
               return HttpResponse(rex.error)
            elif rex.error == 'invalid status code':
               return HttpResponse(rex.error)
            else:
               Student.objects.filter(user__email=request.POST.get("username")).update(NTA_Level = rex.NTA_level,academic_year = rex.academic_year)
               # user.first_name = rex.name
               # user.username = rex.email
               # user.email = rex.email
               # user.password = make_password(request.POST.get("password"))
               # user.save()
               # students.user = user
               # students.regNo = rex.regno
               # students.NTA_Level = rex.NTA_level
               # students.academic_year = rex.academic_year
               # students.mobile = rex.mobile
               # students.gender = rex.gender
               # students.course = rex.level
               # students.save()
               # rex.studentImage(email=request.POST.get("username"), password=request.POST.get("password"))
               # with open(rex.regno+".jpg", 'rb') as f:
               #    django_file = File(f)
               #    os.remove('media/profile_pic/{0}.jpg'.format(rex.regno))
               #    students.photo.save(rex.regno+".jpg", django_file, save=True)
               # os.remove(rex.regno+".jpg")
               user = auth.authenticate(username=email,password=password)
               if user is not None:
                  auth.login(request,user)
                  return redirect('/')
            
         
               return redirect('/login')
         else:
            userr = auth.authenticate(username=email,password=password)
            if userr is not None:
               auth.login(request,userr)
               return redirect('/')
            else:
               messages.info(request,'Unknown information')
               return redirect('/login')
      else:
         
         rex.studentInfo(email=request.POST.get("username"), password=request.POST.get("password"))
         if rex.error == "no internet connection":
            print(rex.error)
            return HttpResponse('no connection')
         elif rex.error == "Login Failed: invalid credentials":
            return HttpResponse(rex.error)
         elif rex.error == 'invalid status code':
            return HttpResponse(rex.error)
         else:
            
            user.first_name = rex.name
            user.username = rex.email
            user.email = rex.email
            user.password = make_password(request.POST.get("password"))
            user.save()
            students.user = user
            students.regNo = rex.regno
            students.NTA_Level = rex.NTA_level
            students.academic_year = rex.academic_year
            students.mobile = rex.mobile
            students.gender = rex.gender
            students.course = rex.level
            students.save()
            rex.studentImage(email=request.POST.get("username"), password=request.POST.get("password"))
            with open(rex.regno+".jpg", 'rb') as f:
               django_file = File(f)
               students.photo.save(rex.regno+".jpg", django_file, save=True)
            os.remove(rex.regno+".jpg")
            user = auth.authenticate(username=email,password=password)
            if user is not None:
               auth.login(request,user)
               return redirect('/')
         
            return redirect('/login')
         
         
      
      
   
   return render(request,'login.html',{'side':'dashboard'})



@login_required(login_url='/login')
def dashboard(request):
   
   s = Student.objects.all()
   return render(request,'html/dist/index.html',{'side':'dashboard','s':s})

@login_required(login_url='/login')
def student(request):
   
   
   return render(request,'html/dist/students.html',{'side':'being'})

@login_required(login_url='/login')
def staff(request):
   
   
   return render(request,'html/dist/staffs.html',{'side':'staff'})
@login_required(login_url='/login')
def department(request):
   
   
   return render(request,'html/dist/departments.html',{'side':'department'})
@login_required(login_url='/login')
def project_type(request):
   
   
   return render(request,'html/dist/project_type.html',{'side':'project_type'})
@login_required(login_url='/login')
def level(request):
   
   
   return render(request,'html/dist/level.html',{'side':'level'})

@login_required(login_url='/login')
def logout(request):
    auth.logout(request)

    return redirect('/login')