import kivy
import time
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import smtplib

Builder.load_string("""
<inputScreen>:


    mission: mission
    days: days

    GridLayout:
        cols:1
        size: root.width , root.height 


        GridLayout:
            cols:2

            Label:
                font_size: 40
                text: "Mission"

            TextInput:
                id: mission
                multiline:False

            Label:
                font_size: 40
                text: "Days"

            TextInput:
                id: days
                multiline:False

        Button:
            size_hint: 0.5,0.5
            font_size: 40

            text:"Save"
            on_press: root.btn()
        Button:
            size_hint: 0.5,0.5
            font_size: 40
            text:"Submit"
            on_press: root.manager.current = 'success'

<outputScreen>:


    GridLayout:

        cols:1
        size: root.width , root.height

        TimeLabel:



        Button:
            size_hint: 0.1,0.1
            font_size: 40
            text: 'Reset'
            on_press: root.manager.current = 'menu'
<TimeLabel>:
    font_size: 200
    x:-545
    y:-475
    color: (0,1,0,1)
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
""")


class inputScreen(Screen):
    mission = ObjectProperty(None)
    days = ObjectProperty(None)

    class MyGrid(Widget):
        pass

    def btn(self):
        print("Name:", self.mission.text, "days:", self.days.text)
        f = open('data.txt', 'w')
        ts = str(time.time())

        if self.days.text != "":
            f.write(self.days.text)
        else:
            f.write("-1")
            f.write('\n')
            f.write('1000')
            myApp().stop()

        f.write('\n')
        f.write(ts)
        f.write('\n')
        f.write(self.mission.text)
        f.close()
        self.mission.text = ""
        self.days.text = ""


class outputScreen(Screen):
    per = '2'

    class MyGrid(Widget):
        pass


class TimeLabel(Label):
    def __init__(self, **kwargs):
        super(TimeLabel, self).__init__(**kwargs)
        f = open("data.txt", "r")
        self.days = float(f.readline())
        self.started = float(f.readline())
        ts = time.time()
        self.total_second = float(self.days * 1440 * 60)
        covered = float(ts - self.started)
        percentage_success = (covered / self.total_second) * 100
        self.text = str(percentage_success)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        f = open("data.txt", "r")
        self.days = float(f.readline())
        self.started = float(f.readline())
        self.mission_name = str(f.readline())
        ts = time.time()
        self.total_second = float(self.days * 1440 * 60)
        covered = float(ts - self.started)
        percentage_success = (covered / self.total_second) * 100
        if percentage_success < 0:
            percentage_success = 100

        self.text = str(round(percentage_success, 2))
        self.text = self.text + '%'
        if round(percentage_success, 2) - int(percentage_success) == 0.0 :
            content = 'Congratulations! You completed :' + self.text
            subject = 'Mission success:' + self.mission_name
            msg = f'Subject: {subject}\n\n{content}'
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('sender@gmail.com', 'Password')
            mail.sendmail('sender@gmail.com', 'receipt@gmail.com', msg)
            mail.close

        print(self.days, self.started,round(percentage_success, 2) - int(percentage_success))
        print(self.text)


# Create the screen manager
sm = ScreenManager()
choice = 1
check = open("data.txt", "r")
abc = int(check.readline())
if abc == -1:
    choice = 0

if choice == 1:
    sm.add_widget(outputScreen(name='success'))
    sm.add_widget(inputScreen(name='menu'))
else:
    sm.add_widget(inputScreen(name='menu'))
    sm.add_widget(outputScreen(name='success'))


class myApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    myApp().run()
