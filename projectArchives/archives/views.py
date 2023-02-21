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
import os
import csv


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

poppler_path = os.path.join(PROJECT_DIR, '..', 'poppler-23.01.0', 'Library', 'bin')
cover = os.path.join(PROJECT_DIR, '..', 'media','coverpage')




def  login(request):
 try:
   user = User()
   students = Student()
   staffs = Staff()
   projects = Project()
 
   
   
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
            if 'diploma' in (rex.level).lower():
                   students.level_id = 2
            students.save()
            us = Student.objects.get(user__username=email)
            print(us.id)
            if 'diploma' in (rex.level).lower() and rex.NTA_level == 6:
                   projects.student_id = students
                   projects.department_id = students.department
                   projects.save()
                  #  doc = Document.objects.create(project=projects)
                  #  Progress.objects.create(document=doc)
            elif 'bachelor' in (rex.level).lower() and rex.NTA_level == 8:
                   projects.student_id = students
                   projects.department_id = students.department
                   projects.save()
                  #  doc = Document.objects.create(project=projects)
                  #  Progress.objects.create(document=doc)
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
   return render(request,'html/dist/login.html')
 except:
    messages.success(request,'Something went wrong')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/login')
def dashboard(request):
   
   s = Student.objects.all().count()
   d = Department.objects.all().count()
   p = Project.objects.all().count()
   f  = Staff.objects.all().count()
   finalB =  Progress.objects.filter()
   finalD =  Student.objects.filter(NTA_Level=6)
   return render(request,'html/dist/index.html',{'side':'dashboard','s':s,'d':d,'f':f,'p':p,'b':finalB,'o':finalD})

@login_required(login_url='/login')
def student(request):
   exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,37]
   p = Permission.objects.exclude(id__in=exclude_perm)
   
   s = Student.objects.all().order_by('NTA_Level')
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
      NTA_Level = request.POST.get('NTA_Level')
      course = request.POST.get('course')
      departments = request.POST.get('department')
      gender = request.POST.get('gender')
      password = make_password("@DIT123")
      users = User.objects.filter(username=email).exists()
      user = Student.objects.filter(regNo=regNo).exists()
      if users and user:
         messages.error(request,'Student exists')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         
      u = User.objects.create(username=email,email=email,password=password,first_name=name)
      Student.objects.create(user=u,regNo=regNo,mobile=mobile,academic_year=academic_year,NTA_Level=NTA_Level,course=course,department_id=departments,gender=gender)
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
   
   d = Department.objects.all()
   return render(request,'html/dist/departments.html',{'side':'department','d':d})


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
   
   levels = Level.objects.all()
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

def reset_password(request,pk):
   password = make_password("@DIT123")
   User.objects.filter(id=pk).update(password=password)
   messages.success(request,'Password reseted successful')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    messages.success(request,'logout successful')
    return redirect('/login')
 
 
def editstaff(request,pk):
#  try:
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
#  except:
#     messages.error(request,'Something went wrong')
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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


def projects(request):
   
   
   return render(request,'html/dist/projects.html')