from pyrebase import initialize_app as p_init
from re import search, fullmatch
from firebase_admin import credentials
from firebase_admin import initialize_app as f_admin_init
from firebase_admin import db, auth, _auth_utils

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
f_admin_init(cred, {"databaseURL": "https://budget-buddy-11-default-rtdb.firebaseio.com"})


firebase = p_init(firebaseConfig)

authent = firebase.auth()

# Checking Email and Password ----------------------------------------------------------
def check(email, pwd):
    paswd_ok = False
    
    while check_mail(email) == True:
        if len(pwd) < 8:
            paswd_ok = False
            break
        
        elif not search("[a-z]", pwd):
            paswd_ok = False
            break

        elif not search("[A-Z]", pwd):
            paswd_ok = False
            break

        elif not search("[0-9]", pwd):
            paswd_ok = False
            break
        
        elif search("%{,}$[;/]\s", pwd):
            paswd_ok = False
            break

        else:
            paswd_ok = True
            break
    
    return paswd_ok

# Checking Email------------------------------------------------------------------------
def check_mail(email):

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if fullmatch(regex,email):
        return True
    else:
        return False
 
# Check User ID 
def check_userID(userid):
    if userid.islower() == True:
        try:
            auth.get_user(uid=userid)
            return 1
        except auth.UserNotFoundError:
            return 0
    else:
        return 2    

#Create User---------------------------------------------------------------------------------
def create_user(user_id,email,paswd, confirm_paswd, disp_name):
    if check_userID(userid=user_id) == 0:
        if check(email,paswd) == True:
            if paswd == confirm_paswd:
                try:
                    auth.create_user(uid = f"{user_id}", email = f"{email}", password = f"{paswd}", display_name = f"{disp_name}")
                    create_db(user_id=user_id,disp_name=disp_name)
                    return 0
                except:
                    return 1   
            else:
                return 2
        else:
            return 3
    else:
        return 4

#Login --------------------------------------------------------------------------------
def login(user_id, paswd):
    try:
        user_details = auth.get_user(user_id)
    except _auth_utils.UserNotFoundError:
        return 1
    except:
        return 3
    else:
        mail = user_details.email
        try:
            authent.sign_in_with_email_and_password(email = mail,password= paswd)
            return 0
        except :
            return 2

# Create Database-----------------------------------------------------------------------
ref = db.reference("Userdata")
def create_db(user_id, disp_name):
    ref.child(f"{user_id}").set({"Name": f"{disp_name}","Number of Transactions":0})

# Settings Data--------------------------------------------------------------------------
def add_setting_data(user_id, setting_data):    
    ref.child(f"{user_id}").child("Settings_data").set(setting_data)

#Forgot Password-------------------------------------------------------------------------
def forgot_paswd(user_email):
    try:
        user_details = auth.get_user_by_email(user_email)
        authent.send_password_reset_email(user_email)
        return 0
    except:
        return 1

# Add Income------------------------------------------------------------------------
def add_income(user_id, td):
    n = ref.child(f"{user_id}").get()
    p = n['Number of Transactions']
    p +=1
    ref.child(f"{user_id}").child("Transaction").child("Income").child(f"{p}").set(td)
    ref.child(f"{user_id}").update({"Number of Transactions":p})

# Add Expense ------------------------------------------------------------------------
def add_expense(user_id, td):
    n = ref.child(f"{user_id}").get()
    p = n['Number of Transactions']
    p +=1
    ref.child(f"{user_id}").child("Transaction").child("Expense").child(f"{p}").set(td)
    ref.child(f"{user_id}").update({"Number of Transactions":p})

# Getting Balance ---------------------------------------------------------------------- 
def balance(user_id):
    inc_ref = db.reference(f'Userdata/{user_id}/Transaction/Income')
    exp_ref = db.reference(f'Userdata/{user_id}/Transaction/Expense')
    exp_details = exp_ref.order_by_key().get()
    inc_details = inc_ref.order_by_key().get()

    total_inc = sum([inc_details[key]['Amount'] for key in inc_details ])
    total_exp = sum([exp_details[key]['Amount'] for key in exp_details ]) 
    
    return total_inc-total_exp


# Getting Display Name ------------------------------------------------------------------
def get_display_name(uid):
    details = auth.get_user(uid)
    return details.display_name
