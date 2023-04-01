from datetime import datetime,date
# from main import descrp, transac_type, method, amount, max_lim, income, rent

max_lim = 1000
income = 10000 
rent = 2000
descrp = "grocery"
transac_type = "Debit"
amount = 500
method = "Gpay"

sd = {
    "Daily Expense Limit": f"{max_lim}",
    "Monthly Income":f"{income}",
    "Rent": f"{rent}"
}

time_now = datetime.now().strftime("%H:%M:%S")
td = {
    "Date": f"{date.today()}",
    "Time": f"{time_now}",
    "Description": f"{descrp}",
    "Credit or Debit": f"{transac_type}",
    "Amount": f"{amount}",
    "Transaction Method":f"{method}"
}
