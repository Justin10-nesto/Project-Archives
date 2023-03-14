import datetime
import json
all = []
for i in range(1,57):
    all.append(i)
data = [    
    {"model": "archives.level","pk": 1,        
"fields": {"name": "BACHELOR DEGREE","date_created":str(datetime.datetime.now().date())}
},
    {        "model": "archives.level","pk": 2,        
"fields": {"name": "ORDINARY DIPLOMA","date_created":str(datetime.datetime.now().date())}
},
    {"model": "archives.Department","pk": 1,        
"fields": {"name": "CIVIL"}
},
    {"model": "archives.Department","pk": 2,        
"fields": {"name": "COMPUTER STUDIES"}
},
 {"model": "archives.Department","pk": 3,        
"fields": {"name": "ELECTRICAL"}
},  
  {"model": "archives.Department","pk": 4,        
"fields": {"name": "ELECTRONICS AND TELECOMMUNICATIONS"}
},  
   {"model": "archives.Department","pk": 5,        
"fields": {"name": "MECHANICAL"}


}, 
   
   {"model": "archives.Department","pk": 6,        
"fields": {"name": "SCIENCE AND LABORATORY TECHNOLOGY"}
} , 
   {
        "model": "auth.group",
        "pk": 6,
        "fields": {
            "name": "Student",
            "permissions": [32,40,52]
        }
    },
   {
        "model": "auth.group",
        "pk": 5,
        "fields": {
            "name": "Final_Year",
            "permissions": [29,32,40,49,52,56]
        }
    },  
   {
        "model": "auth.group",
        "pk": 4,
        "fields": {
            "name": "Staff",
            "permissions": [32,40,52,56]
        }
    }, 
   {
        "model": "auth.group",
        "pk": 3,
        "fields": {
            "name": "Coordinator",
           "permissions": [32,40,52,56,53,54,55,6,7,8,29,30,31,32,37,38,39,49,50,51]
        }
    },
   {
        "model": "auth.group",
        "pk": 2,
        "fields": {
            "name": "HOD",
           "permissions": [9,10,11,12,14,15,16,41,42,43,44,45,46,47,48,32,40,52,56,53,54,55,6,7,8,29,30,31,32,37,38,39,49,50,51]
        }
    }, 
   {
        "model": "auth.group",
        "pk": 1,
        "fields": {
            "name": "Admin",
           "permissions": all
        }
    },  
    
   {"model": "archives.Project_type","pk": 1,        
"fields": {"name": "Hardware","department":2,"date_created":str(datetime.datetime.now().date())}
} , 
   {"model": "archives.Project_type","pk": 2,        
"fields": {"name": "Software | Mobile Application","department":2,"date_created":str(datetime.datetime.now().date())}
} , 
   
{"model": "archives.Project_type","pk": 3,        
"fields": {"name": "Networking","department":2,"date_created":str(datetime.datetime.now().date())}
} , 

{"model": "archives.Project_type","pk": 4,        
"fields": {"name": "Embedded","department":2,"date_created":str(datetime.datetime.now().date())}
} , 
{"model": "archives.Project_type","pk": 5,        
"fields": {"name": "Multimedia","department":2,"date_created":str(datetime.datetime.now().date())}
} ,

{"model": "archives.Project_type","pk": 6,        
"fields": {"name": "Digital Siginal Processing","department":2,"date_created":str(datetime.datetime.now().date())}
} , 
{"model": "archives.Project_type","pk": 7,        
"fields": {"name": "Digital Image Processing","department":2,"date_created":str(datetime.datetime.now().date())}
} ,  
{"model": "archives.Project_type","pk": 8,        
"fields": {"name": "AI| ML| Data Mining","department":2,"date_created":str(datetime.datetime.now().date())}
} , 
   
   ]
with open('seeders.json', 'w') as f:
    json.dump(data, f)
#python manage.py loaddata seeders.json