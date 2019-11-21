import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import requests
import smtplib
from functools import lru_cache
import pyaudio
#print(pyaudio.pa.get_default_input_device())


email_id = {'steve': 'stevedias796@gmail.com', 'sharon': 'feriesharon@gmail.com', 'parijat': 'parijatdeshpande1@gmail.com', 'sneha': 'sneha.singh51234@gmail.com'}
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
engine = pyttsx3.init('sapi5') #microsoft API to take voice
voice = engine.getProperty('voices')
#print(voice[0].id)
engine.setProperty('voice', voice[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak('Good Morning! Steve.')
    elif hour >= 12 and hour < 18:
        speak('Good Afternoon! Steve.')
    else:
        speak('Good evening! Steve.')

    speak('How may I help You')


#@lru_cache(maxsize=20)
def take_command():
    #it takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)  # This filters noise
        r.pause_threshold = 1
        print("Listening....")
        #r.energy_threshold = 2500
        audio = r.listen(source)

    try:
        print("Recognising...")
        query = r.recognize_google(audio, language='en-in')
        print("User said: ", query)
    except Exception as e:
        #print(e)
        print("Say that again please...")
        return "None"
    return query


def ask_password():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)  # This filters noise
        r.pause_threshold = 1
        print("")
        # r.energy_threshold = 2500
        audio = r.listen(source)

    try:
        print("Recognising...")
        query = r.recognize_google(audio, language='en-in')
        print("User said: ", query)
    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query


def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('stevedias796@gmail.com', '**********')
    server.sendmail('stevedias796@gmail.com', email_id[to], content)
    server.close()


if __name__ == '__main__':
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)  # This filters noise
        r.pause_threshold = 1
        # r.energy_threshold = 2500
        print("say now..")
        audio = r.listen(source)

    try:
        print("Recognising...")
        query = r.recognize_google(audio, language='en-in')
        print(query)
        if query != 'Alexa':
            exit()
    except Exception as e:
        # print(e)
        print("Sorry, you cannot proceed")
        exit()

    wish_me()
    while True:
        query = take_command().lower()
        #logic for executing task based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        #speak("Abigail is a good girl")'''
        elif 'open youtube' in query:
            webbrowser.get(chrome_path).open('www.youtube.com')
        elif 'open google' in query:
            webbrowser.get(chrome_path).open('www.google.com')
        elif 'open instagram' in query:
            webbrowser.get(chrome_path).open('instagram.com')
        elif 'open facebook' in query:
            webbrowser.get(chrome_path).open('facebook.com')
        elif 'the time' in query:
            strtime = datetime.datetime.now().strftime("%H %M")
            speak("Sir, The Time is " + strtime)
        elif 'your name' in query:
            speak("My name is Alexa")
        elif 'play sermons' in query or 'sermon' in query:
            music_path = "S:\\sermons\\all sermons"
            songs = os.listdir(music_path)
            song_num = random.randint(0, len(songs))
            print('sermon number:', song_num)
            os.startfile(os.path.join(music_path, songs[song_num]))
        elif 'play music' in query or 'play songs' in query or 'christian music' in query:
            music_path = "S:\\Music"
            songs = os.listdir(music_path)
            song_num = random.randint(0, len(songs)+1)
            print('song num:', song_num)
            os.startfile(os.path.join(music_path, songs[song_num]))
        elif 'how are you' in query:
            speak('I am Fine. How may i help you')
        elif 'who are you' in query:
            speak('My name is alexa, I am your assistant')
        elif 'my name' in query:
            speak('Your Name is Steve')
        elif 'current weather' in query or 'weather report' in query or 'weather in Mumbai' in query or 'today\'s weather' in query:
            api_addr = "https://api.openweathermap.org/data/2.5/weather?q=Mumbai&appid=eef15359e002e413e619049aaf9ff2c7"
            json_data = requests.get(api_addr).json()
            main_weather = json_data['weather'][0]['main']
            weather_des = json_data['weather'][0]['description']
            report = 'Current Weather in Mumbai is. ' + weather_des
            speak(report)
        elif 'send email' in query:
            try:
                speak('to whom do you want to send email?')
                to = take_command().lower()
                speak('What should i say?')
                content = take_command()
                #to = "stevedias796@gmail.com"
                send_email(to, content)
                speak('Your Email has been sent.')
            except Exception as e:
                print(e)
                speak('I am Sorry, I was not able to send your email.')
        elif 'open glory to god' in query or 'open gtg' in query:
            webbrowser.get(chrome_path).open('https://www.gtgchurch.com/')
        elif 'bye' in query:
            speak("It was nice talking with you, hope to see you soon. Bye")
            exit()