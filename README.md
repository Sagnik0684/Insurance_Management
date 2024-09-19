# Insurance Management
### Admin
- Admin account can be created using createsuperuser command.
- After login, admin can view/update/delete customer
- Can view/add/update/delete policy category like Life, Health, Motor, Travel
- Can view/add/update/delete policy
- Can view total policy holder, approved policy holder, disapproved policy holder
- Can approve policy, applied by customer
- Can answer customer question

### Customer
- Create account (no approval required by admin)
- After login, can view all policy that are added by admin.
- If customer likes any policy, then they can apply for it.
- When customer will apply for any policy, it will go into pending status, admin can approve it.
- Customer can check status of his policy under history section
- Customer can ask question from admin. 

---

## HOW TO RUN THIS PROJECT
- Install Python(3.12) (Dont Forget to Tick Add to Path while installing Python)
- Open Terminal and Execute Following Commands :
```
python3 -m pip install -r requirements.txt
```
- Download This Project Zip Folder and Extract it
- Move to project folder in Terminal. Then run following Commands :
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
- Now enter following URL in Your Browser Installed On Your Pc
```
http://127.0.0.1:8000/
```

## CHANGES REQUIRED FOR CONTACT US PAGE
To be updated...


## Disclaimer
This project is developed for demo purpose and it's not supposed to be used in real application.

