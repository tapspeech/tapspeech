# Text to speech
from plyer import battery, tts, vibrator

import os
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from kivy.core.text import LabelBase

from kivy.core.audio import SoundLoader


LabelBase.register(name='NotoSans', fn_regular='NotoSans.otf')

# Size Dimensions based on Samsung Galaxy Note 5
Window.size = (640, 360)
Window.clearcolor = (1, 1, 1, 1)

# Tracks the screen (English/Cantonese) and also the menu (Liquid/Food/Toilet/Bed)
location = 'English_Main'

# Message Function for English Text to Speech
speak_command_message = ''

# Message Function for Cantonese Audio Files
cantonese_message_name = ''

class English_Window(Screen):
    def change_menu(self, menu):
        global location
        location = menu
        if location == 'English_Main':
            self.ids.Thumb_label.text = 'Liquid'
            self.ids.Index_label.text = 'Toilet'
            self.ids.Middle_label.text = 'Food'
            self.ids.Pinky_label.text = 'Bed'
        elif location == 'English_Liquid':
            self.ids.Thumb_label.text = 'Exit'
            self.ids.Index_label.text = 'Water'
            self.ids.Middle_label.text = 'Juice'
            self.ids.Pinky_label.text = 'Milk'
        elif location == 'English_Toilet':
            self.ids.Thumb_label.text = 'Exit'
            self.ids.Index_label.text = 'Urinate'
            self.ids.Middle_label.text = 'Poop'
            self.ids.Pinky_label.text = 'Help'
        elif location == 'English_Food':
            self.ids.Thumb_label.text = 'Exit'
            self.ids.Index_label.text = 'Rice'
            self.ids.Middle_label.text = 'Pork'
            self.ids.Pinky_label.text = 'Chicken'
        elif location == 'English_Bed':
            self.ids.Thumb_label.text = 'Exit'
            self.ids.Index_label.text = 'Down'
            self.ids.Middle_label.text = 'Up'
            self.ids.Pinky_label.text = 'Help'
        else:
            pass

    def button_press(self, button):
        def change_speak_message(message):
            global speak_command_message
            speak_command_message = message

        def speak_message(message='speak_command'):
            if message == 'speak_command':
                global speak_command_message
                tts.speak(speak_command_message)
            else:
                tts.speak(message)

        def change_menu(menu):
            global location
            location = menu
            if location == 'English_Main':
                self.ids.Thumb_label.text = 'Liquid'
                self.ids.Index_label.text = 'Toilet'
                self.ids.Middle_label.text = 'Food'
                self.ids.Pinky_label.text = 'Bed'
            elif location == 'English_Liquid':
                self.ids.Thumb_label.text = 'Exit'
                self.ids.Index_label.text = 'Water'
                self.ids.Middle_label.text = 'Juice'
                self.ids.Pinky_label.text = 'Milk'
            elif location == 'English_Toilet':
                self.ids.Thumb_label.text = 'Exit'
                self.ids.Index_label.text = 'Urinate'
                self.ids.Middle_label.text = 'Poop'
                self.ids.Pinky_label.text = 'Help'
            elif location == 'English_Food':
                self.ids.Thumb_label.text = 'Exit'
                self.ids.Index_label.text = 'Rice'
                self.ids.Middle_label.text = 'Pork'
                self.ids.Pinky_label.text = 'Chicken'
            elif location == 'English_Bed':
                self.ids.Thumb_label.text = 'Exit'
                self.ids.Index_label.text = 'Down'
                self.ids.Middle_label.text = 'Up'
                self.ids.Pinky_label.text = 'Help'
            else:
                pass

        global location
        if button == 'Thumb':
            if location == 'English_Main':
                change_menu('English_Liquid')
                speak_message('Liquid selected')
            elif location == 'English_Liquid':
                change_menu('English_Main')
                speak_message('Exited liquid menu')
                change_speak_message('')
            elif location == 'English_Toilet':
                change_menu('English_Main')
                speak_message('Exited toilet menu')
                change_speak_message('')
            elif location == 'English_Food':
                change_menu('English_Main')
                speak_message('Exited food menu')
                change_speak_message('')
            elif location == 'English_Bed':
                change_menu('English_Main')
                speak_message('Exited bed menu')
                change_speak_message('')
            else:
                pass

        elif button == 'Index':
            if location == 'English_Main':
                change_menu('English_Toilet')
                speak_message('Toilet selected')
            elif location == 'English_Liquid':
                speak_message('Water')
                change_speak_message('Please give me some water')
            elif location == 'English_Toilet':
                speak_message('Urinate')
                change_speak_message('I need to go urinate')
            elif location == 'English_Food':
                speak_message('Rice')
                change_speak_message('Please give me some rice')
            elif location == 'English_Bed':
                speak_message('Down')
                change_speak_message('Please move my bed down')
            else:
                pass

        elif button == 'Middle':
            if location == 'English_Main':
                change_menu('English_Food')
                speak_message('Food selected')
            elif location == 'English_Liquid':
                speak_message('Juice')
                change_speak_message('Please give me some juice')
            elif location == 'English_Toilet':
                speak_message('Poop')
                change_speak_message('I need to go poop')
            elif location == 'English_Food':
                speak_message('Pork')
                change_speak_message('Please give me some pork')
            elif location == 'English_Bed':
                speak_message('Up')
                change_speak_message('Please move my bed up')
            else:
                pass

        elif button == 'Pinky':
            if location == 'English_Main':
                change_menu('English_Bed')
                speak_message('Bed selected')
            elif location == 'English_Liquid':
                speak_message('Milk')
                change_speak_message('Please give me some milk')
            elif location == 'English_Toilet':
                speak_message('Help')
                change_speak_message('Please help me go to the bathroom')
            elif location == 'English_Food':
                speak_message('Chicken')
                change_speak_message('Please give me some chicken')
            elif location == 'English_Bed':
                speak_message('Help')
                change_speak_message('I need help with my bed')
            else:
                pass

        elif button == 'Speak_Command':
            speak_message()
            change_speak_message('')

        elif button == 'Cantonese':
            change_speak_message('')
            location = 'Cantonese'+location.replace('English','')
            screen_two = self.manager.get_screen('Cantonese_Window')
            screen_two.change_menu(location)

class Cantonese_Window(Screen):
    def change_menu(self, menu):
        global location
        location = menu
        if location == 'Cantonese_Main':
            self.ids.Cantonese_Thumb_label.text = '飲品'
            self.ids.Cantonese_Index_label.text = '廁所'
            self.ids.Cantonese_Middle_label.text = '食物'
            self.ids.Cantonese_Pinky_label.text = '教床'
        elif location == 'Cantonese_Liquid':
            self.ids.Cantonese_Thumb_label.text = '離開'
            self.ids.Cantonese_Index_label.text = '水'
            self.ids.Cantonese_Middle_label.text = '果汁'
            self.ids.Cantonese_Pinky_label.text = '其他'
        elif location == 'Cantonese_Toilet':
            self.ids.Cantonese_Thumb_label.text = '離開選擇'
            self.ids.Cantonese_Index_label.text = '“o”尿'
            self.ids.Cantonese_Middle_label.text = '“o”屎'
            self.ids.Cantonese_Pinky_label.text = '其他'
        elif location == 'Cantonese_Food':
            self.ids.Cantonese_Thumb_label.text = '離開選擇'
            self.ids.Cantonese_Index_label.text = '食飯'
            self.ids.Cantonese_Middle_label.text = '豬肉'
            self.ids.Cantonese_Pinky_label.text = '其他'
        elif location == 'Cantonese_Bed':
            self.ids.Cantonese_Thumb_label.text = '離開選擇'
            self.ids.Cantonese_Index_label.text = '教低張床'
            self.ids.Cantonese_Middle_label.text = '教高張床'
            self.ids.Cantonese_Pinky_label.text = '其他'
        else:
            pass

    def button_press(self, button):
        def change_cantonese_message_name(file_name):
            global cantonese_message_name
            cantonese_message_name = file_name

        def speak_message(message='speak_command'):
            global cantonese_message_name
            if message == 'speak_command' and cantonese_message_name == '':
                pass
            elif message == 'speak_command':
                self.sound = SoundLoader.load(os.path.join('cantonese_audio',cantonese_message_name))
                self.sound.play()
                cantonese_message_name = ''
            else:
                self.sound = SoundLoader.load(os.path.join('cantonese_audio',message))
                self.sound.play()

        def change_menu(menu):
            global location
            location = menu
            if location == 'Cantonese_Main':
                self.ids.Cantonese_Thumb_label.text = '飲品'
                self.ids.Cantonese_Index_label.text = '廁所'
                self.ids.Cantonese_Middle_label.text = '食物'
                self.ids.Cantonese_Pinky_label.text = '教床'
            elif location == 'Cantonese_Liquid':
                self.ids.Cantonese_Thumb_label.text = '離開'
                self.ids.Cantonese_Index_label.text = '水'
                self.ids.Cantonese_Middle_label.text = '果汁'
                self.ids.Cantonese_Pinky_label.text = '其他'
            elif location == 'Cantonese_Toilet':
                self.ids.Cantonese_Thumb_label.text = '離開選擇'
                self.ids.Cantonese_Index_label.text = '“o”尿'
                self.ids.Cantonese_Middle_label.text = '“o”屎'
                self.ids.Cantonese_Pinky_label.text = '其他'
            elif location == 'Cantonese_Food':
                self.ids.Cantonese_Thumb_label.text = '離開選擇'
                self.ids.Cantonese_Index_label.text = '食飯'
                self.ids.Cantonese_Middle_label.text = '牛肉'
                self.ids.Cantonese_Pinky_label.text = '其他'
            elif location == 'Cantonese_Bed':
                self.ids.Cantonese_Thumb_label.text = '離開選擇'
                self.ids.Cantonese_Index_label.text = '教低張床'
                self.ids.Cantonese_Middle_label.text = '教高張床'
                self.ids.Cantonese_Pinky_label.text = '其他'
            else:
                pass

        global location
        if button == '拇指':
            if location == 'Cantonese_Main':
                change_menu('Cantonese_Liquid')
                speak_message('你選擇左飲品.mp3')
            elif location == 'Cantonese_Liquid':
                change_menu('Cantonese_Main')
                change_cantonese_message_name('')
                speak_message('離開選擇.mp3')
            elif location == 'Cantonese_Toilet':
                change_menu('Cantonese_Main')
                change_cantonese_message_name('')
                speak_message('離開選擇.mp3')
            elif location == 'Cantonese_Food':
                change_menu('Cantonese_Main')
                change_cantonese_message_name('')
                speak_message('離開選擇.mp3')
            elif location == 'Cantonese_Bed':
                change_menu('Cantonese_Main')
                change_cantonese_message_name('')
                speak_message('離開選擇.mp3')
            else:
                pass

        if button == '食指':
            if location == 'Cantonese_Main':
                change_menu('Cantonese_Toilet')
                speak_message('你選擇左廁所選項.mp3')
            elif location == 'Cantonese_Liquid':
                change_cantonese_message_name('我要飲水.mp3')
                speak_message('你選擇左​水.mp3')
            elif location == 'Cantonese_Toilet':
                change_cantonese_message_name('我要去“o”尿.mp3')
                speak_message('你選擇‘“o”尿選項.mp3')
            elif location == 'Cantonese_Food':
                change_cantonese_message_name('我想​食飯.mp3')
                speak_message('你選擇​食飯.mp3')
            elif location == 'Cantonese_Bed':
                change_cantonese_message_name('請幫我教低張床.mp3')
                speak_message('你選擇教​低​張床.mp3')
            else:
                pass

        if button == '中指':
            if location == 'Cantonese_Main':
                change_menu('Cantonese_Food')
                speak_message('你選擇左食物選項.mp3')
            elif location == 'Cantonese_Liquid':
                change_cantonese_message_name('我想要果汁.mp3')
                speak_message('你選擇左​果汁.mp3')
            elif location == 'Cantonese_Toilet':
                change_cantonese_message_name('我要去“o”屎.mp3')
                speak_message('你選擇‘“o”屎選項.mp3')
            elif location == 'Cantonese_Food':
                change_cantonese_message_name('我想食牛肉.mp3')
                speak_message('你選擇左牛肉.mp3')
            elif location == 'Cantonese_Bed':
                change_cantonese_message_name('請幫我教高張床.mp3')
                speak_message('你選擇教​高​張床.mp3')
            else:
                pass

        if button == '小指':
            if location == 'Cantonese_Main':
                change_menu('Cantonese_Bed')
                speak_message('你選擇左教床選項.mp3')
            elif location == 'Cantonese_Liquid':
                change_cantonese_message_name('你選擇左​其他.mp3')
                speak_message('你過來聽我.mp3')
            elif location == 'Cantonese_Toilet':
                change_cantonese_message_name('你選擇左​其他.mp3')
                speak_message('你過來聽我.mp3')
            elif location == 'Cantonese_Food':
                change_cantonese_message_name('你選擇左​其他.mp3')
                speak_message('你過來聽我.mp3')
            elif location == 'Cantonese_Bed':
                change_cantonese_message_name('你選擇左​其他.mp3')
                speak_message('你過來聽我.mp3')
            else:
                pass

        elif button == 'English':
            location = 'English'+location.replace('Cantonese','')
            screen_one = self.manager.get_screen('English_Window')
            screen_one.change_menu(location)

        if button == 'Speak_Command':
            speak_message()
            change_cantonese_message_name('')

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("Tap_Speech.kv")

class Tap_SpeechApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    Tap_SpeechApp().run()
