from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
import fire 
from kivy.core.text import LabelBase
from kivymd.uix.pickers import MDDatePicker
from database import display_date
from datetime import datetime
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"






LabelBase.register(name='abode',
                   fn_regular='assets/abode.ttf')

from kivymd.theming import ThemableBehavior
from kivymd.uix.datatables import MDDataTable
from kivy.clock import Clock

class MyDataTable(MDDataTable):
        def __init__(self, **kwargs):
            # skip the MDDataTable.__init__() and call its superclass __init__()
            super(ThemableBehavior, self).__init__(**kwargs)
    
            # schedule call to MDDataTable.__init__() contents after ids are populated
            Clock.schedule_once(partial(self.delayed_init, **kwargs))
    
        def delayed_init(self, dt, **kwargs):
            # this is copied from MDDataTable.__init__() with super() call deleted
            self.header = TableHeader(
                column_data=self.column_data,
                sorted_on=self.sorted_on,
                sorted_order=self.sorted_order,
            )
            self.table_data = TableData(
                self.header,
                row_data=self.row_data,
                check=self.check,
                rows_num=self.rows_num,
                _parent=self,
            )
            self.register_event_type("on_row_press")
            self.register_event_type("on_check_press")
            self.pagination = TablePagination(table_data=self.table_data)
            self.table_data.pagination = self.pagination
            self.header.table_data = self.table_data
            self.table_data.fbind("scroll_x", self._scroll_with_header)
            self.ids.container.add_widget(self.header)
            self.ids.container.add_widget(self.table_data)
            if self.use_pagination:
                self.ids.container.add_widget(self.pagination)
            Clock.schedule_once(self.create_pagination_menu, 0.5)
            self.bind(row_data=self.update_row_data)

class Card(MDCard):
    source = StringProperty()
    text = StringProperty()

class ContentNavigationDrawer(BoxLayout):
    pass



class BudgetBuddy(MDApp):
    
    global sm
    sm = ScreenManager()
    
    def dropdown(self):

        self.menu_list = [
            {
                "viewclass":"OneLineListItem",
                "text":'Grocery',
                "on_press" : lambda x=f"Grocery": self.set_item(x),
            },
            {
                "viewclass":"OneLineListItem",
                "text":'Food',
                "on_press" : lambda x=f"Food": self.set_item(x),
            },
            {
                "viewclass":"OneLineListItem",
                "text":'Clothing',
                "on_press" : lambda x=f"Clothing": self.set_item(x),
            },
            {
                "viewclass":"OneLineListItem",
                "text":'Electricity',
                "on_press" : lambda x=f"Electricity": self.set_item(x),
            },
            {
                "viewclass":"OneLineListItem",
                "text":'Fuel',
                "on_press" : lambda x=f"Fuel": self.set_item(x),
            },
            {
                "viewclass":"OneLineListItem",
                "text":'Water',
                "on_press" : lambda x=f"": self.set_item(x),
                "text":'Example 1',
            },
            {
                "viewclass":"OneLineListItem",
                "text":'Rent',
                "on_press" : lambda x=f"Rent": self.set_item(x),
            },
            {
                "viewclass":"OneLineListItem",
                "text":'Others',
                "on_press" : lambda x=f"Others": self.set_item(x),
            }
                   
        ]
        self.menu = MDDropdownMenu(
            caller = self.root.get_screen('expense').ids.drop_btn,
            items = self.menu_list,
            width_mult = 4,
        )
        self.menu.open()
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.accent_palette = "Gray"
        self.USERNAME = " "
        self.usid = ''
        self.Balance = 0
        self.dialog = MDDialog()
        self.speed_dial = {
            "Add Expense" : ["plus","on_release", lambda x: BudgetBuddy.add_expense(self)],
            "Add Income"  : ["cash-plus","on_release", lambda x: BudgetBuddy.add_income(self)],
        }

        self.table = MDDataTable(
            column_data=[
                ("Sr.No", dp(30)),
                ("Date", dp(30)),
                ("Type", dp(30)),
                ("Category", dp(30)),
                ("Amount", dp(30))
            ]
        )
        
        
        # sm.add_widget(Builder.load_file("kv/startup.kv"))
        sm.add_widget(Builder.load_file("kv/home.kv"))
        sm.add_widget(Builder.load_file("kv/profile.kv"))
        sm.add_widget(Builder.load_file("kv/login.kv"))
        sm.add_widget(Builder.load_file("kv/signup.kv"))
        sm.add_widget(Builder.load_file('kv/btn1.kv'))
        sm.add_widget(Builder.load_file("kv/forgot.kv"))
        sm.add_widget(Builder.load_file("kv/expense.kv"))
        sm.add_widget(Builder.load_file("kv/income.kv"))
        sm.add_widget(Builder.load_file("kv/develop.kv"))
        
        return sm
   
        
#--------H O M E   P A G E ----------#      
    def set_item(self, text_item):
        self.root.get_screen("expense").ids.drop_btn.text = text_item
        self.menu.dismiss()
        print(self.root.get_screen("expense").ids.drop_btn.text)   
    
#--------Back To Home------------------------------------------       
    def back(self):
        BudgetBuddy.home(self)

#-------Buttton1----------------------------------------------        
    def btn1(self):
        sm.current= 'btn1'
        sm.transition.direction = 'left'
    def profile(self):      
        sm.current= "profile"
        sm.transition.direction = "left"
    def home(self):
        sm.current = "home2"
        self.root.get_screen('home2').ids.name.text = self.USERNAME
        self.root.get_screen('home2').ids.balance.text = f"{self.Balance}"
        sm.transition.direction = "right"
    def login(self):
        sm.current = "login"
        sm.transition.direction = "left"

    def startup(self):
        sm.current = "startup"
        sm.transition.direction = "right"
    def sign_up(self):
        sm.current = 'sign-up'
        sm.transition.direction = "left"

    def sign_up_check(self, username, email, paswd, conf_pwd):
        userid = f"BB_{username}"
        if fire.signin(user_id=userid,email=email,paswd=paswd,confirm_paswd=conf_pwd,disp_name=username) == 0:
            pass

    def sign_in(self):
        self.usid = self.root.get_screen("login").ids.user.text
        passwd = self.root.get_screen("login").ids.pwd.text
        
        if fire.login(user_id=self.usid,paswd=passwd) == 0 :
            self.USERNAME = fire.get_display_name(self.usid)
            self.Balance = fire.balance(self.usid)
            BudgetBuddy.home(self)
            
        elif fire.login(user_id=self.usid,paswd=passwd) == 1:
            Snackbar(text="Invaild Username").open()
        elif fire.login(user_id=self.usid,paswd=passwd) == 3:
            Snackbar(text="Unknown Error").open()        
        else:
            Snackbar(text = "Invalid Password").open()

    def create_user(self):
        us_name = self.root.get_screen('sign-up').ids.user.text
        pswrd   = self.root.get_screen('sign-up').ids.pwd.text
        email_id= self.root.get_screen('sign-up').ids.email.text
        dis_name = self.root.get_screen('sign-up').ids.dname.text
        conf_pwd = self.root.get_screen('sign-up').ids.cpwd.text
        check = fire.create_user(user_id=us_name,email=email_id,paswd=pswrd,confirm_paswd=conf_pwd,disp_name=dis_name)
        if check == 0:
            BudgetBuddy.login(self)
        elif check == 4:
            Snackbar(text="Username already exists").open()
        elif check == 2 :
            Snackbar(text="Confirm Passowrd doesnt match").open()
        elif check == 3:
            Snackbar(text="Invalid Email id or Password").open()
        elif check ==1:
            Snackbar(text="Unknown Error").open()
    def forgot(self):
        sm.current = 'forgot-pass'
        sm.transition.direction = "left"
    
    def open_dialog(self):
        in_btn = MDFlatButton(text="Income",on_release=self.add_income, on_press= self.close_dialog)
        exp_btn = MDFlatButton(text="Expense",on_release=self.add_expense, on_press= self.close_dialog)
        self.dialog = MDDialog(title = 'ADD',size_hint=(0.7,1),buttons = [in_btn, exp_btn],elevation=0)
        self.dialog.open()
        
    def close_dialog(self,obj):
        self.dialog.dismiss()
    def add_expense(self,obj):
        sm.current = 'expense'
        sm.transition.direction = "left"

    def add_income(self,obj):
        sm.current = 'income'
        sm.transition.direction = "left"
        
    def on_save_income(self,instance,value,date_range):
        a = display_date(value)
        self.root.get_screen('income').ids.date_disp.text= a
    def show_date_picker_income(self):
        date_dialog = MDDatePicker(font_name="assets/Poppins-Medium")  
        date_dialog.bind(on_save=self.on_save_income)
        date_dialog.open()  
    
    def on_save_expense(self,instance,value,date_range):
        a = display_date(value)
        self.root.get_screen('expense').ids.date_disp.text= a
    def show_date_picker_expense(self):
        date_dialog = MDDatePicker(font_name="assets/Poppins-Medium")  
        date_dialog.bind(on_save=self.on_save_expense)
        date_dialog.open()    

    def done_add_expense(self):
        amount = self.root.get_screen('expense').ids.amount.text
        descp = self.root.get_screen('expense').ids.descp.text
        date = self.root.get_screen('expense').ids.date_disp.text
        category = self.root.get_screen("expense").ids.drop_btn.text
        t_data = {
            "Description": f"{descp}",
            "Amount": amount,
            "Category" : f"{category}",
            "Type" : "Expense"
        }
        fire.add_expense(self.usid, td=t_data, date=date)
        self.Balance = fire.balance(self.usid) 
        BudgetBuddy.home(self)

    def done_add_income(self):
        amount = self.root.get_screen('income').ids.amount.text
        descp = self.root.get_screen('income').ids.descp.text
        date = self.root.get_screen('income').ids.date_disp.text
        t_data = {
            "Description": f"{descp}",
            "Amount": amount,
            "Type": "Income"
        }
        fire.add_expense(self.usid, td=t_data , date = date)
        self.Balance = fire.balance(self.usid)
        BudgetBuddy.home(self)
        
    def on_save_btn1(self,instance,value,date_range):
        a = display_date(value)
        self.root.get_screen('btn1').ids.btn_date.text= a
    def show_date_picker_btn1(self):
        date_dialog = MDDatePicker(font_name="assets/Poppins-Medium")  
        date_dialog.bind(on_save=self.on_save_btn1)
        date_dialog.open()   
BudgetBuddy().run()
