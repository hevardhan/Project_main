from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel,MDIcon
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.relativelayout import MDRelativeLayout

import fire 
from plyer import filechooser
from database import display_date




Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"



kv ='''
<Card>
    orientation: 'vertical'
    radius: 15
    padding: '8dp'
    size_hint: None, None
    size: "200dp", "100dp"
    ripple_behavior: True
    md_bg_color: 'red'
    Image:
        source: root.source
    MDLabel:
        text: root.text
        halign: 'center'
        font_size: '13sp'
        adaptive_height: True
        font_name: 'assets/Poppins-Medium'
'''


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
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.file_manager_obj = MDFileManager(
            select_path =self.select_path,
            exit_manager=self.exit_manager,
            preview=True
        )
        
    def select_path(self,path):
        fire.export(user_id="hevardhan",pswd="12345678",path=path)
        self.exit_manager(self)
    def open_file_manager(self):
        self.file_manager_obj.show("/")
        
    
    def exit_manager(self,obj):
        self.file_manager_obj.close()
    
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
                "on_press" : lambda x=f"Water": self.set_item(x),
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
        self.USERNAME = "Hevardhan"
        self.usid = 'hevardhan'
        self.Balance = 0
        self.dialog = MDDialog()
        self.speed_dial = {
            "Add Expense" : ["plus","on_release", lambda x: BudgetBuddy.add_expense(self)],
            "Add Income"  : ["cash-plus","on_release", lambda x: BudgetBuddy.add_income(self)],
        }
        
        
        # sm.add_widget(Builder.load_file("kv/startup.kv"))
        sm.add_widget(Builder.load_file("kv/home.kv"))
        sm.add_widget(Builder.load_file("kv/graph1.kv"))
        sm.add_widget(Builder.load_file("kv/profile.kv"))
        sm.add_widget(Builder.load_file("kv/login.kv"))
        sm.add_widget(Builder.load_file("kv/signup.kv"))
        sm.add_widget(Builder.load_file('kv/btn1.kv'))
        sm.add_widget(Builder.load_file("kv/forgot.kv"))
        sm.add_widget(Builder.load_file("kv/expense.kv"))
        sm.add_widget(Builder.load_file("kv/income.kv"))
        sm.add_widget(Builder.load_file("kv/develop.kv"))
        Builder.load_string(kv)
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
        
        date_btn = self.root.get_screen('btn1').ids.btn_date.text
        try:
            list_disp = fire.history_per_day(user_id="hevardhan",date=date_btn)
        except KeyError:
            len_list = 0
            Snackbar(text="No Record").open()
        else:
            len_list = len(list_disp)
            self.root.get_screen('btn1').ids.md_list.rows = len_list
        for i in range(len_list):
            self.root.get_screen('btn1').ids.md_list.add_widget(
                MDCard(
                    MDRelativeLayout(
                            MDLabel(
                                text="Button",
                                adaptive_size=True,
                                color="grey",
                                pos=("12dp", "12dp"),
                    )
                  ),
                  line_color=(0.2, 0.2, 0.2, 0.8),
                  padding="8dp",
                  size_hint=(None, None),
                  size=("200dp", "100dp"),
                  radius = 15,
                orientation = 'vertical',
                )
            )

    def profile(self):      
        sm.current= "profile"
        sm.transition.direction = "left"
        self.root.get_screen('profile').ids.prof_name.text = self.USERNAME
        self.root.get_screen('profile').ids.prof_usid.text = self.usid
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
            Snackbar(text="Confirm Password doesnt match").open()
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
        try:
            list_disp = fire.history_per_day(user_id="hevardhan",date=a)
        except KeyError:
            len_list = 0
            Snackbar(text="No Record").open()
        else:
            len_list = len(list_disp)
            self.root.get_screen('btn1').ids.md_list.rows = len_list
            for i in range(len_list):
                amount = list_disp[i]['Amount']
                descp  = list_disp[i]['Description']
                # cat    = list_disp[i]['Category'] 
                mode   = list_disp[i]['Type']
                self.root.get_screen('btn1').ids.md_list.add_widget(
                    MDCard(
                        MDRelativeLayout(
                                MDLabel(
                                    text=f"{amount}",
                                    adaptive_size=True,
                                    color="grey",
                                    pos_hint={'center_y':.9,'center_x':.47}
                                ),
                                MDIcon(
                                    icon = 'currency-rupee',
                                    pos_hint={'center_y':.9}
                                ),
                                MDLabel(
                                    text=f"{descp}",
                                    adaptive_size=True,
                                    color="grey",
                                    pos_hint={'center_y':.4,'center_x':.47}
                                ),
                                MDIcon(
                                    icon = 'note',
                                    pos_hint={'center_y':.4}
                                ),
                                MDLabel(
                                    text=f"{mode}",
                                    adaptive_size=True,
                                    color="grey",
                                    pos_hint={'center_y':.1}
                                )
                    ),
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    padding="8dp",
                    size_hint=(None, None),
                    size=("200dp", "100dp"),
                    radius = 15,
                    orientation = 'vertical',
                    )
                )

    def show_date_picker_btn1(self):
        date_dialog = MDDatePicker(font_name="assets/Poppins-Medium")  
        date_dialog.bind(on_save=self.on_save_btn1)
        date_dialog.open()
        self.root.get_screen('btn1').ids.md_list.clear_widgets()

BudgetBuddy().run()
