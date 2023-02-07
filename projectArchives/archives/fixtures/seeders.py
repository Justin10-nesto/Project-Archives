import datetime
import json
data = [    
    {"model": "archives.level","pk": 1,        
"fields": {"name": "BEING","date_created":str(datetime.datetime.now().date())}
},
    {        "model": "archives.level","pk": 2,        
"fields": {"name": "OD","date_created":str(datetime.datetime.now().date())}
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
}  
   ]
with open('seeders.json', 'w') as f:
    json.dump(data, f)
#python manage.py loaddata seeders.json