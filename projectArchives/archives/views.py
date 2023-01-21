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

#@login_required(login_url='/login')
def  login(request):
   user = User()
   students = Student()
   staffs = Staff()
   if request.method == 'POST':
      rex.studentInfo(email=request.POST.get("username"), password=request.POST.get("password"))
      if rex.error == "no internet connection":
         return HttpResponse('no connection')
      elif rex.error == "Login Failed: invalid credentials":
         return HttpResponse(rex.error)
      elif rex.error == 'invalid status code':
         return HttpResponse(rex.error)
      else:
         print(rex.error)
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
         students.save()
         rex.studentImage(email=request.POST.get("username"), password=request.POST.get("password"))
         with open(rex.regno+".jpg", 'rb') as f:
            django_file = File(f)
            students.photo.save(rex.regno+".jpg", django_file, save=True)
         os.remove(rex.regno+".jpg")
      
         return redirect('/')
         
         
      
      
   
   return render(request,'login.html',{'side':'dashboard'})

def dashboard(request):
   
   s = Student.objects.all()
   return render(request,'html/dist/index.html',{'side':'dashboard','s':s})

def student(request):
   
   
   return render(request,'html/dist/students.html',{'side':'student'})

def staff(request):
   
   
   return render(request,'html/dist/staffs.html',{'side':'student'})

