# content-management-api
Run requirements.txt to install all necessary packages API.

1.To create User:
    method : POST,
    url : "http://127.0.0.1:8000/api/user/register",
    data : {
        "full_name":"Shweta Ayre2",
        "email_id" :"shweta2@gmail.com",
        "phone":"1238764434",
        "password" :"Shweta22",
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
    data : {
        "title":"Title Nnew",
        "body" :"",
        "summary":"1238764434",
        "categories":"cat1,cat2,cat3",
        "document":File
    }

5.To get data of content: 
    method : GET 
    url : "http://127.0.0.1:8000/api/content/1"

6. To delete content: 
   method: DELETE 
   url : "http://127.0.0.1:8000/api/content/1"

7. Search API: 
   method : GET 
   url : "http://127.0.0.1:8000/api/content/content-list?search=asd" 
   
8. To create admin user:
    python3 manage.py loaddata admin_user.jsons