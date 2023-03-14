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
from django.shortcuts import HttpResponseRedirect
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
from django.http import JsonResponse
from pdf2image import convert_from_path
import csv
from fuzzywuzzy import fuzz
import requests

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

poppler_path = os.path.join(PROJECT_DIR, '..', 'poppler-23.01.0', 'Library', 'bin')
cover = os.path.join(PROJECT_DIR, '..', 'media','coverpage')
profile = os.path.join(PROJECT_DIR, '..', 'media','profile_pic')


def check_connection():
       try:
        response = requests.get('http://www.google.com')
        if response.status_code == 200:
              return True
       except:
          pass
       
       return False
           

def login(request):
 try:
   user = User()
   students = Student()
   staffs = Staff()
   projects = Project()
 
   role8 = Group.objects.get(name='Final_Year')
   role = Group.objects.get(name='Student') 
   is_connected = check_connection()
   print(is_connected)
   if is_connected==True:
    if request.method == 'POST':
     if is_connected==True:
      email=request.POST.get("username")
      password=request.POST.get("password")
      users = User.objects.filter(username=email).exists()
      
      u = User.objects.filter(username=email)
      
      u = user.first_name.split(',')
      u = u
      
      current_date = datetime.datetime.now().date()
      october = datetime.datetime(current_date.year,10,1).date()
      
   
      if users:
         us = User.objects.get(username=email)
         if us.is_staff==False:
            if current_date >=october:
               rex.studentInfo(email=request.POST.get("username"), password=request.POST.get("password"))
               if rex.error == "no internet connection":
                  messages.error(request,rex.error)
                  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
               elif rex.error == "Login Failed: invalid credentials":
                  messages.error(request,rex.error)
                  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
               elif rex.error == 'invalid status code':
                  messages.error(request,rex.error)
                  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
               else:
                  Student.objects.filter(user__email=request.POST.get("username")).update(NTA_Level = rex.NTA_level,academic_year = rex.academic_year)
                  user = auth.authenticate(username=email,password=password)
                  if user is not None:
                     auth.login(request,user)
                     messages.success(request,'Login successful')
                     return redirect('/')
               
            
                  return redirect('/login')
            else:
               userr = auth.authenticate(username=email,password=password)
               if userr is not None:
                  auth.login(request,userr)
                  messages.success(request,'Login successful')
                  return redirect('/')
               else:
                  messages.error(request,'Unknown information')
                  return redirect('/login')
         else:
               userr = auth.authenticate(username=email,password=password)
               if userr is not None:
                  auth.login(request,userr)
                  messages.success(request,'Login successful')
                  return redirect('/')
               else:
                  messages.error(request,'Unknown information')
                  return redirect('/login') 
      else:
         
         rex.studentInfo(email=request.POST.get("username"), password=request.POST.get("password"))
         if rex.error == "no internet connection":
               messages.error(request,rex.error)
               return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         elif rex.error == "Login Failed: invalid credentials":
               messages.error(request,rex.error)
               return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         elif rex.error == 'invalid status code':
               messages.error(request,rex.error)
               return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         else:
            
            user.first_name = rex.name
            user.username = rex.email
            user.email = rex.email
            user.password = make_password(request.POST.get("password"))
            user.save()
            # if rex.NTA_level == '8' or (rex.NTA_level=='6' and 'diploma' in (rex.level).lower()):
            #        user.groups.add(role8)
            # else:
            user.groups.add(role) 
            # course = (rex.level).split()
            # course = course[-2] +" "+ course[-1]
            # print(course)
            students.user = user
            students.regNo = rex.regno
            students.NTA_Level = rex.NTA_level
            students.academic_year = rex.academic_year
            students.mobile = rex.mobile
            students.gender = rex.gender
            students.course = rex.level
         
            if 'computer' in (rex.level).lower() or 'information' in (rex.level).lower() or 'multimedia' in (rex.level).lower():
               students.department_id = 2
            elif 'civil' in (rex.level).lower() or 'mining' in (rex.level).lower() or 'gas' in (rex.level).lower():
               students.department_id = 1
            elif 'electrical' in (rex.level).lower() or 'biomedical' in (rex.level).lower() or 'renewable' in (rex.level).lower():
               students.department_id = 3
            elif 'electronics' in (rex.level).lower() or 'communication' in (rex.level).lower():
               students.department_id = 4
            elif 'mechanical' in (rex.level).lower():
                students.department_id = 5
            elif 'food' in (rex.level).lower() or 'laboratory' in (rex.level).lower() or 'biotechnology' in (rex.level).lower():
               students.department_id = 6
            if 'bachelor' in (rex.level).lower():
                   students.level_id = 1
            else:
                   students.level_id = 2
            students.save()
            # us = Student.objects.get(user__username=email)
            # print(f'{rex.NTA_level}:{rex.level}')
            # if rex.NTA_level == '6' and 'diploma' in (rex.level).lower():
            #        projects.student_id = us.id
            #        projects.department_id = us.department_id
                  
            #       #  projects.save()
            #       #  doc = Document.objects.create(project=projects)
            #       #  Progress.objects.create(document=doc)
            # if 'bachelor' in (rex.level).lower() and rex.NTA_level == '8':
            #         projects.student_id = us.id
            #         projects.department_id = us.department_id
                  
            # projects.save()  
            # p = Project.objects.get(student_id=us.id)
            # Document.objects.create(project_id=p.id)
            # f = Document.objects.get(project_id=p.id)
            # Progress.objects.create(document_id=f.id)
            rex.studentImage(email=request.POST.get("username"), password=request.POST.get("password"))
            
            with open(rex.regno+".jpg", 'rb') as f:
               
               django_file = File(f)
               students.photo.save(rex.regno+".jpg", django_file, save=True)
            os.remove(rex.regno+".jpg")
            user = auth.authenticate(username=email,password=password)
            if user is not None:
               auth.login(request,user)
               messages.success(request,'Login successful')
               return redirect('/')
         
            return redirect('/login')
     else: 
        messages.error(request,'No internet Connection')
        return render(request,'html/dist/login.html')         
    return render(request,'html/dist/login.html')
   else:
      messages.error(request,'No internet Connection')
      return render(request,'html/dist/login.html')    
 except:
    messages.error(request,'Something went wrong')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/login')
def dashboard(request):
   
   s = Student.objects.all().count()
   d = Department.objects.all().count()
   if request.user.is_superuser:
          
    p = Project.objects.all().count()
   else:
      p = Project.objects.filter(department_id=request.user.student.department.id).count() or Project.objects.filter(department_id=request.user.staff.department.id).count()    
   f  = Staff.objects.all().count()
   finalB =  Progress.objects.all()
   finalD =  Student.objects.filter(NTA_Level=6)
   k = request.POST.dict()
   print(k)
   return render(request,'html/dist/index.html',{'side':'dashboard','s':s,'d':d,'f':f,'p':p,'b':finalB,'o':finalD})

@login_required(login_url='/login')
def student(request):
   exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,37]
   p = Permission.objects.exclude(id__in=exclude_perm)
   
   s = Student.objects.all().order_by('id')
   d = Department.objects.all()
   g = Group.objects.all()
   
   return render(request,'html/dist/students.html',{'side':'being','s':s,'d':d,'g':g,'p':p})

@login_required(login_url='/login')
def student_od(request):
   exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,37]
   p = Permission.objects.exclude(id__in=exclude_perm)
   s = Student.objects.filter(NTA_Level__lte=6,NTA_Level__gte=4)
   d = Department.objects.all()
   g = Group.objects.all()
   
   return render(request,'html/dist/students_od.html',{'side':'od','s':s,'d':d,'g':g,'p':p})

@login_required(login_url='/login')
def addstudent(request):
 try:
   if request.method == "POST":
      
      name = request.POST.get('name')
      email = request.POST.get('username')
      regNo = request.POST.get('regno')
      mobile = request.POST.get('mobile')
      academic_year = request.POST.get('academic_year')
      NTA_Level = int(request.POST.get('NTA_Level'))
      course = request.POST.get('course')
      departments = request.POST.get('department')
      gender = request.POST.get('gender')
      password = make_password("@DIT123")
      users = User.objects.filter(username=email).exists()
      user = Student.objects.filter(regNo=regNo).exists()
      if users and user:
         messages.error(request,'Student exists')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      if NTA_Level==8:
       u = User.objects.create(username=email,email=email,password=password,first_name=name)
       
       Student.objects.create(user=u,regNo=regNo,mobile=mobile,academic_year=academic_year,level_id=1,NTA_Level=NTA_Level,course=course,department_id=departments,gender=gender)
       messages.success(request,'Student created successful')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      elif NTA_Level==6:
       u = User.objects.create(username=email,email=email,password=password,first_name=name)
       Student.objects.create(user=u,regNo=regNo,mobile=mobile,academic_year=academic_year,level_id=2,NTA_Level=NTA_Level,course=course,department_id=departments,gender=gender)
       messages.success(request,'Student created successful')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      elif NTA_Level>6:
       u = User.objects.create(username=email,email=email,password=password,first_name=name)
       Student.objects.create(user=u,regNo=regNo,mobile=mobile,academic_year=academic_year,level_id=1,NTA_Level=NTA_Level,course=course,department_id=departments,gender=gender)
       messages.success(request,'Student created successful')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      elif NTA_Level <=6:
       u = User.objects.create(username=email,email=email,password=password,first_name=name)
       Student.objects.create(user=u,regNo=regNo,mobile=mobile,academic_year=academic_year,level_id=2,NTA_Level=NTA_Level,course=course,department_id=departments,gender=gender)
       messages.success(request,'Student created successful')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
 except:
    messages.error(request,'Something went wrong')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def addstaff(request):

   if request.method == "POST":
      
      name = request.POST.get('name')
      email = request.POST.get('username')
      staff_id = request.POST.get('staff_id')
      mobile = request.POST.get('mobile')
      level = request.POST.get('level')
      # NTA_Level = request.POST.get('NTA_Level')
      # course = request.POST.get('course')
      departments = request.POST.get('department')
      gender = request.POST.get('gender')
      
      group_id = request.POST.get('role')
      print(group_id)
      group = Group.objects.get(id=group_id)
      password = make_password("@DIT123")
      users = User.objects.filter(username=email).exists()
      user = Staff.objects.filter(staff_id=staff_id).exists()
      if users and user:
         messages.error(request,'Staff exists')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      # images = convert_from_path('C:\\Users\\Raphael\\OneDrive\\Desktop\\file\\pdf\\RSM.pdf',poppler_path=poppler_path)

      # # Save pages as images in the pdf
      # images[0].save(f'{cover}\\page' +'.jpg', 'JPEG') 
      u = User.objects.create(username=email,email=email,password=password,first_name=name)
      Staff.objects.create(user=u,staff_id=staff_id,mobile=mobile,department_id=departments,gender=gender,level=level)
      u.groups.add(group)
   
      messages.success(request,'Staff created successful')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#  except:
#     messages.error(request,'Something went wrong')
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 
 
@login_required(login_url='/login')
def editstudent(request,pk):
   
 try:
   r=User.objects.get(id=pk)
   u = Group.objects.all()
   d=Student.objects.filter(user__id=pk)
   p =Student.objects.get(user__id=pk)
   t = Permission.objects.all()
   if request.method=='POST':
      name = request.POST.get('name')
      email = request.POST.get('username')
      regNo = request.POST.get('regno')
      mobile = request.POST.get('mobile')
      academic_year = request.POST.get('academic_year')
      NTA_Level = request.POST.get('NTA_Level')
      course = request.POST.get('course')
      departments = request.POST.get('department')
      gender = request.POST.get('gender')
      users = User.objects.get(id=pk)
      user = Student.objects.get(user_id=pk)
      User.objects.filter(id=pk).update(username=email,email=email,first_name=name)
      Student.objects.filter(user_id=pk).update(regNo=regNo,mobile=mobile,academic_year=academic_year,NTA_Level=NTA_Level,course=course,department_id=departments,gender=gender)
      for i in Group.objects.all():
             p.user.groups.remove(i.id)
             
      for j in Permission.objects.all():
              p.user.user_permissions.remove(j.id)
      
             
      s_id = []
      r_id=[]
      permission = [x.name for x in Group.objects.all()]
      perm = [i.name for i in Permission.objects.all()]
      for x in permission:
             
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
      for i in perm:
             
             r_id.append(int(request.POST.get(i))) if request.POST.get(i) else print("")
      for s in s_id:
           p.user.groups.add(Group.objects.get(id=s)) 
      for r in r_id:
           p.user.user_permissions.add(Permission.objects.get(id=r))    
      messages.success(request,'Student updated successful')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 except:
      messages.error(request,'Something went wrong | exist')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
   
   
@login_required(login_url='/login')
def staff(request):
   l = Level.objects.all()
   
   exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,37]
   p = Permission.objects.exclude(id__in=exclude_perm)
   s = Staff.objects.all()
   d = Department.objects.all()
   g = Group.objects.all()
   
   return render(request,'html/dist/staffs.html',{'side':'staff','s':s,'d':d,'g':g,'p':p,'l':l})

@login_required(login_url='/login')
def department(request):
   try:
      if request.method=='POST':
            name = request.POST['name']
            Department.objects.create(name=name)
            messages.success(request,'Department Added successful')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      d = Department.objects.all().order_by('id')
      return render(request,'html/dist/departments.html',{'side':'department','d':d})
   except:
      messages.error(request,'Something Went Wrong')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def deletedepartment(request,pk):
   try:
      Department.objects.filter(id=pk).delete()
      messages.success(request,'deleted successful')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
   except:
       messages.error(request,'something went wrong')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

@login_required(login_url='/login')
def editdepartment(request,pk):
   try:
      if request.method=='POST':
         name = request.POST.get('name')
         Department.objects.filter(id=pk).update(name=name)
         messages.success(request,'updated successful')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
   except:
       messages.error(request,'something went wrong') 
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))     

@login_required(login_url='/login')
def project_type(request):
   t = Project_type.objects.values('department__name','name','id').order_by('id')
   p = Permission.objects.all()
   d = Department.objects.all()
   return render(request,'html/dist/project_type.html',{'side':'project_type','d':d,'t':t})

@login_required(login_url='/login')
def addprojecttype(request):
 try:
   
   if request.method == "POST":
      name = request.POST.get("name")
      department = request.POST.get("department") 
      Project_type.objects.create(name=name,department_id=department)
      messages.success(request,'Project Type added successful')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
 except:
      messages.error(request,'something is wrong')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
@login_required(login_url='/login')
def editprojecttype(request,pk):
   
   if request.method == "POST":
      name = request.POST.get("name")
      department = request.POST.get("department") 
      if request.user.is_superuser == True:
       Project_type.objects.filter(id=pk).update(name=name,department_id=department)
       messages.success(request,'Project Type edited successful')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      else:
        Project_type.objects.filter(id=pk).update(name=name)
        messages.success(request,'Project Type edited successful')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  
 

@login_required(login_url='/login')
def deleteprojecttype(request,pk):
 try:
      Project_type.objects.filter(id=pk).delete()
      messages.success(request,'Project Type deleted successful')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
 except:
      messages.error(request,'something is wrong')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

@login_required(login_url='/login')
def level(request):
   
   levels = Level.objects.all().order_by('id')
   return render(request,'html/dist/level.html',{'side':'level','level':levels})

@login_required(login_url='/login')
def deletelevel(request,pk):
   try:
      Level.objects.filter(id=pk).delete()
      messages.success(request,'deleted successful')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
   except:
       messages.error(request,'something went wrong')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

@login_required(login_url='/login')
def editlevel(request,pk):
   try:
      if request.method=='POST':
         name = request.POST.get('name')
         Level.objects.filter(id=pk).update(name=name)
         messages.success(request,'updated successful')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
   except:
       messages.error(request,'something went wrong') 
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  
    
@login_required(login_url='/login')
def addlevel(request):
   try:
      if request.method=='POST':
         name = request.POST.get('name')
         Level.objects.create(name=name)
         messages.success(request,'level created successful')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
   except:
       messages.error(request,'something went wrong') 
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    

@login_required(login_url='/login')
def deletestudent(request,pk):
   User.objects.filter(id=pk).delete()
   messages.success(request,'User deleted successful')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/login')
def delete_level(request,pk):
   try:
      Level.objects.filter(id=pk).delete()
      messages.success(request,'deleted successful')
      return redirect('/level')
   except:
       messages.error(request,'something went wrong')

@login_required(login_url='/login')
def update_level(request,pk):
   try:
      if request.method=='POST':
         name = request.POST.get('name')
         Level.objects.filter(id=pk).update(name=name)
         messages.success(request,'updated successful')   
         return redirect('/level')
   except:
       messages.error(request,'something went wrong')
 
 
@login_required(login_url='/login')
def manageroles(request):
       
      g = Group.objects.all().order_by('id')
      exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24]
      p = Permission.objects.exclude(id__in=exclude_perm)
      
      return render(request,'html/dist/manageroles.html',{'side':'role','p':p,'g':g})

@login_required(login_url='/login')
def addroles(request):
  try:
   p = Group()
   if request.method == "POST":
      name = request.POST.get("name")
      permission = [x.name for x in Permission.objects.all()]
      s_id = []
      p.name=name
      for x in permission:
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
      p.save()
      for s in s_id:
           p.permissions.add(Permission.objects.get(id=s))   
      messages.success(request,'Role added successful')
      return redirect('/manageroles')  
  except:
      messages.error(request,'something is wrong')


@login_required(login_url='/login')
def editroles(request,pk):
   
  try:
   exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,37]
   p = Permission.objects.exclude(id__in=exclude_perm)
   r = Group.objects.filter(id=pk)
   y=Group.objects.get(id=pk)
   if request.method == 'POST':
    name = request.POST.get('name')
    
             
    for j in Permission.objects.all():
              y.permissions.remove(j.id) 
      
      
    permission = [x.name for x in Permission.objects.all()]
     
    s_id = []
    Group.objects.filter(id=pk)
    for x in permission:
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
    r=Group.objects.filter(id=pk).update(name=name)
      
    for s in s_id:
           y.permissions.add(Permission.objects.get(id=s))  
    messages.success(request,'Login successful')
    return redirect('/manageroles')
           
   return render(request,'html/dist/editroles.html',{'r':r,'p':p})
  except:
      messages.error(request,'Something is wrong')

@login_required(login_url='/login')     
def blockuser(request,pk):
       
     
      try:
         u = User.objects.filter(id=pk).filter(is_active='True')
         if u:      
            User.objects.filter(id=pk).update(is_active='False')
            messages.success(request,'block successful')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
         else:
            User.objects.filter(id=pk).update(is_active='True') 
            messages.success(request,'Activation successful') 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      except: 
       messages.error(request,'Something went Wrong')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')   
def deleteroles(request,pk):
    
    g = Group.objects.filter(id=pk).delete()
    if g:
       messages.success(request,'Role deleted successful')
    
    return redirect('/manageroles')
@login_required(login_url='/login')
def reset_password(request,pk):
   password = make_password("@DIT123")
   User.objects.filter(id=pk).update(password=password)
   messages.success(request,'Password reseted successful')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    messages.success(request,'logout successful')
    return redirect('/login')
 
@login_required(login_url='/login')
def editstaff(request,pk):
 try:
   if request.method == "POST":
      
      name = request.POST.get('name')
      email = request.POST.get('username')
      staff_id = request.POST.get('staff_id')
      mobile = request.POST.get('mobile')
      level = request.POST.get('level')
      # NTA_Level = request.POST.get('NTA_Level')
      # course = request.POST.get('course')
      departments = request.POST.get('department')
      gender = request.POST.get('gender')
      
      group_id = request.POST.get('roles')
      
      group = Group.objects.get(id=group_id)
      
      password = make_password("@DIT123")
      users = User.objects.filter(username=email).exists()
      user = Staff.objects.filter(staff_id=staff_id).exists()
      # if users and user:
      #    messages.error(request,'Staff exists')
      #    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         
      User.objects.filter(id=pk).update(username=email,email=email,first_name=name)
      Staff.objects.filter(user_id=pk).update(staff_id=staff_id,mobile=mobile,department_id=departments,gender=gender,level=level)
      u = User.objects.get(id=pk)
      for i in Group.objects.all():
             u.groups.remove(i.id)
      u.groups.add(group)
      messages.success(request,'Staff created successful')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 except:
    messages.error(request,'Something went wrong')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def upload_addstaff(request):
        if request.method == 'POST':
         file_data = request.FILES['file']
         decoded_file = file_data.read().decode('utf-8').splitlines()
         reader = csv.DictReader(decoded_file)
         for row in reader:
                dept_id = Department.objects.get(name=row['department'])
                role_id = Group.objects.get(name=row['role'])
                user = User.objects.create(
                    first_name=row['name'],
                    email=row['email'],
                    username=row['email'],
                    is_staff = True  ,
                    password = make_password('@DIT123'),
                    
                )
                
                u = User.objects.get(username=row['email'])
                u.groups.add(role_id,)
                Staffs = Staff.objects.create(
                    user = user,
                    gender=row['gender'],
                    staff_id=row['staff_id'],
                    mobile = row['mobile'],
                    department = dept_id ,
                     
                )
                
        messages.success(request,'Staff created successful')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def upload_student(request):
      try:
        if request.method == 'POST':
         file_data = request.FILES['file']
         decoded_file = file_data.read().decode('utf-8').splitlines()
         reader = csv.DictReader(decoded_file)
         for row in reader:
                dept_id = Department.objects.get(name=row['Department'])
                role_id = Group.objects.get(name="Student")
                users = User.objects.filter(username=row['Email']).exists()
                user = Student.objects.filter(regNo=row['Registration Number']).exists()
                if user and users:
                       continue
                else:
                
                 user = User.objects.create(
                    first_name=row['Name'],
                    email=row['Email'],
                    username=row['Email'],
                    password = make_password('@DIT123'),
                    
                )
                
                u = User.objects.get(username=row['email'])
                u.groups.add(role_id,)
                Student.objects.create(
                    user = user,
                    gender=row['Gender'],
                    regNo=row['Registration Number'],
                    course = row['Course'],
                    mobile = row['Mobile'],
                    department = dept_id , 
                    academic_year = row['Academic Year'],
                    NTA_Level = int(row['NTA_Level'])    
                )
                
        messages.success(request,'Student created successful')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      except:
         messages.success(request,'The csv should contain Department,Registration Number, Name, Course, Academic Year,Gender,Mobile,NTA_Level,Email')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def projects(request):
   
   d = Document.objects.all()
   f = Department.objects.all()
   s = Student.objects.values_list('academic_year',flat=True).distinct()
   s = list(s)
   g = Project_type.objects.filter(department_id = request.user.student.department.id)
   
   name = request.POST.get('department')
   g = Project_type.objects.filter(department__name = name)
   return render(request,'html/dist/projects.html',{'side':'projects','d':d,'f':f,'s':s,'g':g})

@login_required(login_url='/login')
def changepassword(request):
   if request.method =='POST':
      old = request.POST.get("old")
      new = request.POST.get("new")
      comf = request.POST.get("comf")
      # print(request.user.check_password(old))
      if (request.user.check_password(old)):
       if (new == comf): 
         User.objects.filter(username=request.user.username).update(password=make_password(new))
         messages.success(request,'successful password changed login again')
         return redirect('/login')
       else:
           messages.error(request,'Password Dont Match')
           return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      else:
         messages.error(request,'Check Your Old Password')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      
def upload(request):
   if request.method == 'POST':
      
      
      image= request.FILES.get("file")
      Document.objects.create(project_id=1, file=image)
   s = Student.objects.all().count()
   d = Department.objects.all().count()
   p = Project.objects.all().count()
   f  = Staff.objects.all().count()
   finalB =  Progress.objects.all()
   finalD =  Student.objects.filter(NTA_Level=6)
   return render(request,'html/dist/project.html',{'side':'dashboard','s':s,'d':d,'f':f,'p':p,'b':finalB,'o':finalD})
   
import PyPDF2
import docx2txt
from fuzzywuzzy import fuzz

def check_file_similarity(file_path):
    
    similarity_scores = []
   
    # extract text content from PDF files
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            file_content = ''
            for page in pdf_reader.pages:
                file_content += page.extract_text()
                
    # extract text content from Word files
    elif file_path.endswith('.docx'):
        file_content = docx2txt.process(file_path)
        
    # other file types not supported
    else:
        raise ValueError('Unsupported file type')
    
    for obj in Document.objects.all():
        # extract text content from object file
        if obj.file.path.endswith('.pdf'):
            with open(obj.file.path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                obj_content = ''
                for page in pdf_reader.pages:
                    obj_content += page.extract_text()
        elif obj.file.path.endswith('.docx'):
            obj_content = docx2txt.process(obj.file.path)
        else:
            continue
        name = (obj.file.name)[9:]
        
        # calculate similarity score
        similarity_score = fuzz.token_set_ratio(obj_content, file_content)
        similarity_scores.append((name, similarity_score))
   
    return similarity_scores


  


# def upload(request):
#     above= []
   
#     if request.method == 'POST':  
#         file = request.FILES['file'].read()
#         fileName= request.POST['filename']
#         existingPath = request.POST['existingPath']
#         end = request.POST['end']
#         nextSlice = request.POST['nextSlice']
        
#         if fileName == "":
#             res = JsonResponse({'data':'Invalid Request'})
#             return res
#         else:
#             if existingPath == 'null':
#                 path = 'media/projects/' + fileName
                
#                 if path.endswith('.pdf'):
#                   with open(path, 'wb+') as destination: 
#                      destination.write(file)
#                   FileFolder = Document()
#                   project = Project()
#                   similarity_scores = check_file_similarity(path)
#                   print(request.user.student.id)
#                   if len(similarity_scores)==0:
#                         project.student_id = request.user.student.id
#                         project.department_id = request.user.student.department.id
#                         project.save()
#                         FileFolder.project_id = project.id
#                         FileFolder.file = f'projects\\{fileName}'
                        
#                         #  FileFolder.project_id = end
#                         #  FileFolder.name = fileName
                        
#                         images = convert_from_path(path,poppler_path=poppler_path)
#                         r = random.randint(1,100)
#                         name = f'page{r}'+'.jpg'
#                         path = f'{cover}\\{name}' 
                        
                        
#                         # Save pages as images in the pdf
#                         images[0].save(path) 
#                         FileFolder.cover = name
                        
#                         FileFolder.save()
#                         if int(end):
#                            res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName})
                           
                           
#                         else:
#                            res = JsonResponse({'existingPath': fileName})
#                         return res   
#                   else:
#                      if max(similarity_scores,key=lambda x:x[1])[1] == 100:
#                             res = JsonResponse({'data':'File Exists','existingPath': fileName})
                      
#                      elif max(similarity_scores,key=lambda x:x[1])[1] > 80:
#                         res = JsonResponse({'data':max(similarity_scores,key=lambda x:x[1]),'existingPath': fileName})
                        
#                      else:
#                         FileFolder.file = f'projects\\{fileName}'
                        
#                         #  FileFolder.project_id = end
#                         #  FileFolder.name = fileName
                        
#                         images = convert_from_path(path,poppler_path=poppler_path)
#                         r = random.randint(1,100)
#                         name = f'page{r}'+'.jpg'
#                         path = f'{cover}\\{name}' 
                        
                        
#                         # Save pages as images in the pdf
#                         images[0].save(path) 
#                         FileFolder.cover = name
#                         FileFolder.save()
#                         if int(end):
#                            res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName})
#                         else:
#                            res = JsonResponse({'existingPath': fileName})
#                         return res
#                      return res
#                 else:
#                   res = JsonResponse({'messages':messages.success(request,'ONly pdf required')})
#                   return res

#             else:
#                 path = 'media/' + existingPath
#                 model_id = File.objects.get(existingPath=existingPath)
#                 if model_id.name == fileName:
#                     if not model_id.eof:
#                         with open(path, 'ab+') as destination: 
#                             destination.write(file)
#                         if int(end):
#                             model_id.eof = int(end)
#                             model_id.save()
#                             res = JsonResponse({'data':'Uploadeds Successfully','existingPath':model_id.existingPath})
#                         else:
#                             res = JsonResponse({'existingPath':model_id.existingPath})    
#                         return res
#                     else:
#                         res = JsonResponse({'data':'EOF found. Invalid request'})
#                         return res
#                 else:
#                     res = JsonResponse({'data':'No such file exists in the existingPath'})
#                     return res
#     return render(request, 'html/dist/upload.html')
   
   
def pdf_upload(request):
    p  = Project_type.objects.filter(department_id=request.user.student.department.id)
    role = Group.objects.get(name='Student') 
    if request.method == 'POST' and request.FILES['pdf']:
        title = request.POST.get('title')
        type = request.POST.get('type')
        file = request.FILES.get('pdf').read()
        pdf = request.FILES['pdf']
        path = 'media/projects/' + str(pdf)
        if path.endswith('.pdf'):
         with open(path, 'wb+') as destination: 
                     destination.write(file)
         pdf2 = PyPDF2.PdfReader(path)
         text2 = ''
         # for page in range(number_of_pages):
         text2 += pdf2.pages[0].extract_text()
         # print(text2.strip())
         if 'DAR ES SALAAM INSTITUTE OF TECHNOLOGY' in text2:
            
            project = Project()
            similarity_scores = check_file_similarity(path)         
            if len(similarity_scores)==0:
               images = convert_from_path(path,poppler_path=poppler_path)
               name = str(pdf)[-6:-4]
               names = f'{name}'+'.jpg'
               paths = f'{cover}\\{names}' 
               project.title = title.title()
               project.student_id = request.user.student.id
               project.department_id = request.user.student.department.id
               project.project_type_id = type
               project.save()         
               p =User.objects.get(id=request.user.id)
               for i in Group.objects.all():
                 p.user.groups.remove(i.id)
               p.user.groups.add(role)
               images[0].save(paths) 
               profile = os.path.join(PROJECT_DIR, '..', 'media','projects')
               os.remove(f'{profile}\\{str(pdf)}')        
               pdf_file = Document(cover=names,file=pdf,project_id = project.id )
               pdf_file.save()
               messages.success(request, 'Your PDF was uploaded successfully!')
               #os.remove(path)
               return render(request, 'html/dist/pdf_upload.html', {'pdf_file': pdf_file})
            else:
                        # if max(similarity_scores,key=lambda x:x[1])[1] == 100:
                        #       messages.error(request, 'File Exists')
                        #       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                        
                        if max(similarity_scores,key=lambda x:x[1])[1] > 80:
                           print(f'projects/{max(similarity_scores,key=lambda x:x[1])[0]}')
                           d = Document.objects.get(file=f'projects/{max(similarity_scores,key=lambda x:x[1])[0]}')
                           print(d)
                           messages.error(request, f'Your file is {max(similarity_scores,key=lambda x:x[1])[1]} %  resemble with project with title {d.project.title.title()} of year {d.project.student.academic_year} {d.project.student.level.name.title()} from {d.project.student.department.name.title()} Department')
                           # profile = os.path.join(PROJECT_DIR, '..', 'media','projects')
                           # os.remove(f'{profile}\\{str(pdf)}') 
                           # res = JsonResponse({'data':max(similarity_scores,key=lambda x:x[1]),'existingPath': fileName})
                           return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                           
                        else:
                           images = convert_from_path(path,poppler_path=poppler_path)
                           name = str(pdf)[-6:-4]
                           name = f'{name}'+'.jpg'
                           paths = f'{cover}\\{name}' 
                           project.title = title.title()
                           project.student_id = request.user.student.id
                           project.department_id = request.user.student.department.id
                           project.project_type_id = type
                           project.save()  
                           p =User.objects.get(id=request.user.id)
                           for i in Group.objects.all():
                            p.groups.remove(i.id)
                           p.groups.add(role)  
                           # Save pages as images in the pdf
                           images[0].save(paths) 
                           profile = os.path.join(PROJECT_DIR, '..', 'media','projects')
                           os.remove(f'{profile}\\{str(pdf)}')           
                           pdf_file = Document(cover=name,file=pdf,project_id = project.id )
                           pdf_file.save()
                           messages.success(request, 'Your PDF was uploaded successfully!')
                           
                           return render(request, 'html/dist/pdf_upload.html', {'pdf_file': pdf_file})
         else:
            messages.error(request, 'Upload your document with cover page') 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  
        else:
            messages.error(request, 'only Pdf file required') 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  
    j = Document.objects.filter(project__student_id=request.user.student.id).exists()     
    return render(request, 'html/dist/pdf_upload.html',{'side':'upload_project','p':p,'j':j})
 
 
def preview_pdf(request,pk):
    
   d = Document.objects.filter(id=pk)
    
   
        
   return render(request, 'html/dist/previewed.html',{'side':'a','d':d})

def submissionTime(request):
   # try:
    ids = []
    role8 = Group.objects.get(name='Final_Year')
    role = Group.objects.get(name='Student') 
    if request.method == 'POST':
          date = request.POST.get('date')
          time = request.POST.get('time')
          y,m,d = date.split("-")
          h,mm = time.split(":")
          date = datetime.datetime(int(y),int(m),int(d),int(h),int(mm))
          if request.user.staff.level.id == '':
            messages.error(request, 'Data') 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
          t = Submission.objects.create(date=date,time=time,level_id=request.user.staff.level.id)
          if t:
            for s in (Student.objects.filter(level_id =request.user.staff.level.id) and Student.objects.filter(department_id =request.user.staff.department.id)):
               print(s.id)
               if s.NTA_Level == 8:
                     for i in Group.objects.all():
                                 s.user.groups.remove(i.id)   
                     s.user.groups.add(role8) 
               elif s.NTA_Level == 6:
                        for i in Group.objects.all():
                                 s.user.groups.remove(i.id)
                        s.user.groups.add(role8)  
               
            messages.success(request, 'data saved successful') 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
   # except:
   #          messages.error(request, 'data saved successful') 
   #          return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 


def my_view(request):
    # Retrieve a Time model instance (assuming it exists)
   time_instance = Submission.objects.filter(level_id=request.user.staff.level.id).first()

    # Pass the date and time values to the template
    
   date=time_instance.date.strftime('%Y-%m-%d')
   print(date)
   time=time_instance.time.strftime('%H:%m')
   y,m,d = date.split("-")
   h,mm = time.split(":")
   datt = datetime.datetime(int(y),int(m),int(d),int(h),int(mm))
   now = datetime.datetime.now()

   return render(request, 'html/dist/b.html', {'date':datt,'now':now})

def get_project_types(request, department):
    project_types = Project_type.objects.filter(department__name=department)
    data = [{'id': p.id, 'name': p.name} for p in project_types]
    return JsonResponse({'project_types': data})