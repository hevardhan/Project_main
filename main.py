from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
import fire 

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
        
        sm.add_widget(Builder.load_file("kv/startup.kv"))
        sm.add_widget(Builder.load_file("kv/home2.kv"))
        sm.add_widget(Builder.load_file("kv/profile.kv"))
        sm.add_widget(Builder.load_file("kv/login.kv"))
        sm.add_widget(Builder.load_file("kv/signup.kv"))
        sm.add_widget(Builder.load_file('kv/btn1.kv'))
        sm.add_widget(Builder.load_file("kv/forgot.kv"))

        return sm
   
        
#--------H O M E   P A G E ----------#         
    
#--------Back To Home------------------------------------------       
    def back(self):
        BudgetBuddy.home(self)

#-------Buttton1----------------------------------------------        
    def btn1(self):
        sm.current= 'btn1'
        sm.transition.direction = 'left'

#        
    def profile(self):
        sm.current= "profile"
        sm.transition.direction = "left"
    def home(self):
        sm.current = "home2"
        sm.transition.direction = "right"
        self.root.get_screen('home2').ids.name.text = self.USERNAME
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
        self.USERNAME = username
        if fire.check(username,passwd) == True:
            if fire.login(user_id=username,paswd=passwd):
                BudgetBuddy.home(self,username)
            else:
                Snackbar(text="Login Failed").open()
        else:
            Snackbar(text = "Username or Password Invalid").open()

    def create_user(self):
        us_name = self.root.get_screen('sign-up').ids.user.text
        pswrd   = self.root.get_screen('sign-up').ids.pwd.text
        email_id= self.root.get_screen('sign-up').ids.email.text
        dis_name = self.root.get_screen('sign-up').ids.dname.text
        conf_pwd = self.root.get_screen('sign-up').ids.cpwd.text
        self.USERNAME = us_name
        check = fire.create_user(user_id=us_name,email=email_id,paswd=pswrd,confirm_paswd=conf_pwd,disp_name=dis_name)
        if check == 0:
            pass
        elif check == 1:
            Snackbar(text="Username already exists").open()
        elif check == 2 :
            Snackbar(text="Confirm Passowrd doesnt match").open()
        elif check == 4:
            Snackbar(text="Invalid Email id or Password").open()
        
    def forgot(self):
        sm.current = 'forgot-pass'
        sm.transition.direction = "left"


            
BudgetBuddy().run()
