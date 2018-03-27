import pytesseract
from gtts import gTTS
import speech_recognition as sr
import pygame
from pygame import mixer
from PIL import Image

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import  Label
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

class olayUyg(App):
    Window.size = (480, 800)
    kontrol=False

    #Mikrofondan Dosyanın ismini alır.
    def Konusma(self):

        try:
            mixer.init()
            mixer.music.load('Dosyalar/x.wav')
            mixer.music.play()

            r = sr.Recognizer()


            with sr.Microphone() as source:
                audio = r.listen(source)

            konusma = r.recognize_google(audio, language="tr")
            print(konusma)
            return konusma

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        except:
            print('Kelime Algılanamadı')
            mixer.init()
            mixer.music.load('Dosyalar/x.wav')
            mixer.music.play()
            self.dugme.bind(on_press=self.Tikla)

    # Resimdeki yazıyı String hale getirir. Dosya uzantısı png olmak zorunda.
    def ResmiAl(self, konusma):
        try:

            isim = konusma
            tur = ".png"
            dosya = isim + tur

            Resim = Image.open('Resimler/' + dosya)

            Son = pytesseract.image_to_string(Resim, lang="tur")
            return Son, isim

        except:
            print('Resim Dönüştürülemedi')
            mixer.init()
            mixer.music.load('Dosyalar/x.wav')
            mixer.music.play()
            self.dugme.bind(on_press=self.Tikla)


    # Yazıyı seslendirip mp3 dosyasına çevirir.
    def Seslendir(Self, Son, isim):
        try:
            mixer.init()
            mixer.music.load('Dosyalar/ses.mp3')
            mixer.music.play()

            tts = gTTS(text=Son, lang='tr')
            belge = isim + ".mp3"
            tts.save('Dosyalar/Ses Dosyaları/' + belge)

            mixer.init()
            mixer.music.load(belge)
            mixer.music.play()

        except:
            print('Yazı Seslendirilemedi')
            mixer.init()
            mixer.music.load('Dosyalar/x.wav')
            mixer.music.play()
            self.dugme.bind(on_press=self.Tikla)


    # Ekrana ikinci tıklayışta fonksiyonların çalıştırılması.
    def Tikla(self, nesne):
        mixer.music.stop()

        try:
            x = self.Konusma()
            y = self.ResmiAl(x)
            self.Seslendir(y[0],y[1])

        except:
            print('Dönüştürme Yapılamadı')
            mixer.init()
            mixer.music.load('Dosyalar/x.wav')
            mixer.music.play()
            self.dugme.bind(on_press=self.Tikla)

    # Ekrana ilk tıklayışta çalışacak kullanım yönlendirmesi
    def Giris(self,nesne):
        if(self.kontrol==False):
            mixer.init()
            mixer.music.load('Dosyalar/resim.mp3')
            mixer.music.play()
        self.kontrol=True
        self.dugme.bind(on_press=self.Tikla)

    # Kivy build
    def build(self):

        self.duzen = FloatLayout()
        self.dugme = Button(text = '', background_normal = 'Dosyalar/bg.png')
        self.durum = Label(text = '')

        self.dugme.bind(on_press=self.Giris)

        self.duzen.add_widget(self.dugme)
        self.duzen.add_widget(self.durum)

        return self.duzen


olayUyg().run()
