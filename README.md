# content-management-api
Run requirements.txt to install all necessary packages API.

1.To create User:
    method : POST,
    url : "http://127.0.0.1:8000/api/user/register",
    data : {
        "full_name":"Shweta Ayre2",
        "email_id" :"shweta2@gmail.com",
        "phone":"1238764434",
        "password" :"",
        "address"  :"ff",
        "city":"Mumbai",
        "state":"Maharashtra",
        "country":"India",
        "pincode":"400104"
    
    }

2. User Login: 
    method : POST,
    url : "http://127.0.0.1:8000/api/user/login",
    data :{email_id,password}


3. To create Author Content :
    method : POST,
    url : "http://127.0.0.1:8000/api/content/create",
    headers:{Authorization:"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6InNod2V0YUBnbWFpbC5jb20iLCJleHAiOjE2MDg4OTkzNDYsImVtYWlsX2lkIjoic2h3ZXRhQGdtYWlsLmNvbSJ9.W5tLpyr2eHZbHh7-VlTbBSoqMxlqdI3B0iLYLbmklMo"}
    data : {
        "title":"Title Nnew",
        "body" :"",
        "summary":"1238764434",
        "categories":"cat1,cat2,cat3",
        "document":File
    }

4.To update author content :
    method : PUT,
    url : "http://127.0.0.1:8000/api/content/1",
    headers:{Authorization:"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6InNod2V0YUBnbWFpbC5jb20iLCJleHAiOjE2MDg4OTkzNDYsImVtYWlsX2lkIjoic2h3ZXRhQGdtYWlsLmNvbSJ9.W5tLpyr2eHZbHh7-VlTbBSoqMxlqdI3B0iLYLbmklMo"}
    data : {
        "title":"Title Nnew",
        "body" :"",
        "summary":"1238764434",
        "categories":"cat1,cat2,cat3",
        "document":File
    }

5.To get data of content: 
    headers:{Authorization:"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6InNod2V0YUBnbWFpbC5jb20iLCJleHAiOjE2MDg4OTkzNDYsImVtYWlsX2lkIjoic2h3ZXRhQGdtYWlsLmNvbSJ9.W5tLpyr2eHZbHh7-VlTbBSoqMxlqdI3B0iLYLbmklMo"}
    method : GET 
    url : "http://127.0.0.1:8000/api/content/1"

6. To delete content: 
   method: DELETE 
   headers:{Authorization:"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6InNod2V0YUBnbWFpbC5jb20iLCJleHAiOjE2MDg4OTkzNDYsImVtYWlsX2lkIjoic2h3ZXRhQGdtYWlsLmNvbSJ9.W5tLpyr2eHZbHh7-VlTbBSoqMxlqdI3B0iLYLbmklMo"}
   url : "http://127.0.0.1:8000/api/content/1"

7. Search API: 
   method : GET
   headers:{Authorization:"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6InNod2V0YUBnbWFpbC5jb20iLCJleHAiOjE2MDg4OTkzNDYsImVtYWlsX2lkIjoic2h3ZXRhQGdtYWlsLmNvbSJ9.W5tLpyr2eHZbHh7-VlTbBSoqMxlqdI3B0iLYLbmklMo"}
   url : "http://127.0.0.1:8000/api/content/content-list?search=asd" 
   
8. To create admin user:
    python3 manage.py loaddata admin_user.jsons
