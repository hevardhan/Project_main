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
        
        sm.add_widget(Builder.load_file("kv/startup.kv"))
        sm.add_widget(Builder.load_file("kv/home2.kv"))
        sm.add_widget(Builder.load_file("kv/profile.kv"))
        sm.add_widget(Builder.load_file("kv/login.kv"))
        sm.add_widget(Builder.load_file("kv/signup.kv"))
        sm.add_widget(Builder.load_file('kv/btn1.kv'))
        sm.add_widget(Builder.load_file("kv/forgot.kv"))

        return sm
    def display_name(self, user_name):
        self.root.get_screen('home2').ids.name.text = user_name
#--------H O M E   P A G E ----------#         
    class HomePage(MDApp):
        def __init__(hom,name):
            hom.Username = name
        def back(hom):
            BudgetBuddy.home(hom)
        def btn1(hom):
            sm.current= 'btn1'
            sm.transition.direction = 'left'
        def profile(hom):
            sm.current= "profile"
            sm.transition.direction = "left"
        def home(hom):
            sm.current = "home2"
            sm.transition.direction = "right"
            BudgetBuddy.display_name(super.self(),hom.Username)
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
        
        if (us_name == "chris"):
            BudgetBuddy.HomePage(us_name).home()

    def forgot(self):
        sm.current = 'forgot-pass'
        sm.transition.direction = "left"


            
BudgetBuddy().run()
