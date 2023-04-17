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

Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"


LabelBase.register(name='abode',
                   fn_regular='assets/abode.ttf')
class Card(MDCard):
    source = StringProperty()
    text = StringProperty()

class ContentNavigationDrawer(BoxLayout):
    pass



class BudgetBuddy(MDApp):
    
    global sm

    
    sm = ScreenManager()
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.accent_palette = "Gray"
        self.USERNAME = " "
        self.speed_dial = {
            "Add Expense" : ["plus","on_release", lambda x: BudgetBuddy.add_expense(self)],
            "Add Income"  : ["cash-plus","on_release", lambda x: BudgetBuddy.add_income(self)],
        }

        # sm.add_widget(Builder.load_file("kv/startup.kv"))
        sm.add_widget(Builder.load_file("kv/home.kv"))
        sm.add_widget(Builder.load_file("kv/profile.kv"))
        sm.add_widget(Builder.load_file("kv/login.kv"))
        sm.add_widget(Builder.load_file("kv/signup.kv"))
        sm.add_widget(Builder.load_file('kv/btn1.kv'))
        sm.add_widget(Builder.load_file("kv/forgot.kv"))
        sm.add_widget(Builder.load_file("kv/expense.kv"))
        sm.add_widget(Builder.load_file("kv/income.kv"))
        
        return sm
   
        
#--------H O M E   P A G E ----------#         
    
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
        username = self.root.get_screen("login").ids.user.text
        passwd = self.root.get_screen("login").ids.pwd.text
        
        if fire.login(user_id=username,paswd=passwd) == 0 :
            self.USERNAME = fire.get_display_name(username)
            BudgetBuddy.home(self)
            
        elif fire.login(user_id=username,paswd=passwd) == 1:
            Snackbar(text="Invaild Username").open()
        elif fire.login(user_id=username,paswd=passwd) == 3:
            Snackbar(text="Unknown Error").open()        
        else:
            Snackbar(text = "Invalid Password").open()

    def create_user(self):
        us_name = self.root.get_screen('sign-up').ids.user.text
        pswrd   = self.root.get_screen('sign-up').ids.pwd.text
        email_id= self.root.get_screen('sign-up').ids.email.text
        dis_name = self.root.get_screen('sign-up').ids.dname.text
        conf_pwd = self.root.get_screen('sign-up').ids.cpwd.text
        self.USERNAME = dis_name
        check = fire.create_user(user_id=us_name,email=email_id,paswd=pswrd,confirm_paswd=conf_pwd,disp_name=dis_name)
        if check == 0:
            BudgetBuddy.home(self)
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

    def add_expense(self):
        sm.current = 'expense'
        sm.transition.direction = "left"

    def add_income(self):
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
        t_data = {
            "Date": f"{date}",
            "Description": f"{descp}",
            "Amount": f"{amount}"
        }
        fire.add_expense(self.USERNAME, td=t_data)  
BudgetBuddy().run()
