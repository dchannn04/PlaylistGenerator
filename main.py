from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.tests.test_clock import callback
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from database import DataBase
from plistgenerator import get_related_artists
from plistgenerator import get_id_for_artist
from plistgenerator import get_artists_for_playlist
from plistmain import generate



class ButtonWindow(Screen):

    song_title = ObjectProperty(None)


    def generate(self):

        print("You entered =>", self.song_title.text)

        generate("Song Title", "BPMGen", "test")



    def swap(self):

        wm.current = "login"





class CreateAccount(Screen):

    username = ObjectProperty(None)

    email = ObjectProperty(None)

    password = ObjectProperty(None)



    def submit(self):

        if self.username.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:

            if self.password != "":

                db.add_user(self.email.text, self.password.text, self.username.text)



                self.reset()



                wm.current = "login"

            else:

                invalidForm()

        else:

            invalidForm()



    def login(self):

        self.reset()

        wm.current = "login"



    def reset(self):

        self.username.text = ""

        self.email.text = ""

        self.password.text = ""







class LoginWindow(Screen):

    email = ObjectProperty(None)

    password = ObjectProperty(None)



    def loginBtn(self):

        if db.validate(self.email.text, self.password.text):

            ButtonWindow.current = self.email.text

            self.reset()

            wm.current = "Start"

        else:

            invalidLogin()



    def createBtn(self):

        self.reset()

        wm.current = "create"



    def reset(self):

        self.email.text = ""

        self.password.text = ""







class WindowManager(ScreenManager):

    pass





def invalidLogin():

    pop = Popup(title='Invalid Login', content=Label(text='Invalid username or password.'), size_hint=(None, None), size=(350, 350))

    pop.open()





def invalidForm():

    pop = Popup(title='Invalid Form', content=Label(text='Please fill in all inputs with valid information.'), size_hint=(None, None), size=(350, 350))

    pop.open()





kv = Builder.load_file("my.kv")

wm = WindowManager()

db = DataBase("users.txt")



screens = [ButtonWindow(name="Start"), LoginWindow(name="login"), CreateAccount(name="create")]

for screen in screens:

    wm.add_widget(screen)



wm.current = "Start"





class MyMainApp(App):

    def build(self):

        return wm





if __name__ == "__main__":

    MyMainApp().run()