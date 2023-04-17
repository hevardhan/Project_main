from datetime import datetime,date
# from main import descrp, transac_type, method, amount, max_lim, income, rent

max_lim = 1000
income = 10000 
rent = 2000
descrp = "Salary"
transac_type = "Debit"
amount = 500
method = "Gpay"

sd = {
    "Daily Expense Limit": f"{max_lim}",
    "Monthly Income":f"{income}",
    "Rent": f"{rent}"
}

time_now = datetime.now().strftime("%H:%M:%S")

def tran_data():    
    td = {
    "Date": f"{date.today()}",
    "Time": f"{time_now}",
    "Description": f"{descrp}",
    "Amount": f"{income}",
    "Transaction Method":f"{method}"
    }

def display_date(get_date):
    date_dis = get_date
    if date_dis.month == 1:
        month = "Jan"
    elif date_dis.month == 2:
        month = "Feb"
    elif date_dis.month == 3:
        month = 'Mar'
    elif date_dis.month == 4:
        month = 'Apr'
    elif date_dis.month == 5:
        month = 'May'
    elif date_dis.month == 6:
        month = 'Jun'
    elif date_dis.month == 7:
        month = 'Jul'
    elif date_dis.month == 8:
        month = 'Aug'
    elif date_dis.month == 9:
        month = 'Sep'
    elif date_dis.month == 10:
        month = 'Oct'
    elif date_dis.month == 11:
        month = 'Nov'
    elif date_dis.month == 12:
        month = 'Dec'
    else:
        raise Exception("Error While Getting Date")

    disp_var = f"{date_dis.day} {month} {date_dis.year}"
    return disp_var
