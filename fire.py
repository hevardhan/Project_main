import pyrebase
import firebase_admin
import re
from firebase_admin import credentials
from firebase_admin import db
from verify_email import verify_email
from firebase_admin import auth
import database

# Firebase Configurationcand Credentials---------------------------------------------------------------
firebaseConfig = {
  "apiKey": "AIzaSyCpjyclqZqiL5lkrEGH5KZEwyli3NXNJI0",
  "authDomain": "budget-buddy-11.firebaseapp.com",
  "databaseURL": "https://budget-buddy-11-default-rtdb.firebaseio.com",
  "projectId": "budget-buddy-11",
  "storageBucket": "budget-buddy-11.appspot.com",
  "messagingSenderId": "994473005551",
  "appId": "1:994473005551:web:cf14c6d203454ec627661a",
  "measurementId": "G-6EYJ0B0PXS"
}

cred = credentials.Certificate('budget-buddy-key.json')

# Initializing Firebase------------------------------------------------------------------
firebase_admin.initialize_app(cred, {"databaseURL": "https://budget-buddy-11-default-rtdb.firebaseio.com"}  )


firebase = pyrebase.initialize_app(firebaseConfig)

authent = firebase.auth()

# user_id = "chris"
# user_email = "chris@gmail.com"
# user_pwd = "Chris123"


# Checking Email and Password ----------------------------------------------------------
def check(email, pwd):

    paswd_ok = False

    while verify_email(email) == True:
        if len(pwd) <= 8:
            paswd_ok = False
            break
        
        elif not re.search("[a-z]", pwd):
            paswd_ok = False
            break

        elif not re.search("[A-Z]", pwd):
            paswd_ok = False
            break

        elif not re.search("[0-9]", pwd):
            paswd_ok = False
            break
        
        elif re.search("%{,}$[;/]\s", pwd):
            paswd_ok = False
            break

        else:
            paswd_ok = True
            break
    
    return paswd_ok

# Checking Email------------------------------------------------------------------------
def check_mail(email):
    if verify_email(email) == True:
        return True
    else:
        return False

def check_user(userid):
    try:
        auth.get_user(userid)
        return True
    except:
        return False
#Signin---------------------------------------------------------------------------------
def signin(user_id,email,paswd, confirm_paswd, disp_name):
    if check(email,paswd) == True:
        if paswd == confirm_paswd:
            if check_user(user_id)==False:
                try:
                    auth.create_user(uid = f"{user_id}", email = f"{email}", password = f"{paswd}", display_name = f"{disp_name}")
                    return 0
                except:
                    return 1
            else:
                return 3
        else:
            return 2
    else:
        return 4

#Login --------------------------------------------------------------------------------
def login(user_id, paswd):
    try:
        user_details = auth.get_user(user_id)
        mail = user_details.email
        authent.sign_in_with_email_and_password(email = mail,password= paswd)
        
        return 0
    except:
        return 1 


#Forgot Password-------------------------------------------------------------------------
def forgot_paswd(user_email):
    try:
        user_details = auth.get_user_by_email(user_email)
        authent.send_password_reset_email(user_email)
        return 0
    except:
        return 1

# Forgot UserID-------------------------------------------------------------------------

# Create Database-----------------------------------------------------------------------
# datab = firebase.database()
ref = db.reference("Userdata")

def create_db(user_id, disp_name, setting_data):
    ref.child(f"{user_id}").set({"Name": f"{disp_name}","Number of Transactions":0})
    ref.child(f"{user_id}").child("Settings_data").set(setting_data)


# Add Transaction------------------------------------------------------------------------
def add_trans(user_id, td):
    n = ref.child(f"{user_id}").get()
    p = n['Number of Transactions']
    p +=1
    ref.child(f"{user_id}").child("Transaction").child(f"{p}").set(td)
    ref.child(f"{user_id}").update({"Number of Transactions":p})


# create_db(user_id="chris", disp_name="Chris Evans", setting_data=database.sd)
# add_trans(user_id="chris",td= database.td)


    