import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ec
import wolframalpha
import requests

# Initialize pyttsx3 engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Set the desired speed
desired_speed = 110
engine.setProperty('rate', desired_speed)

def speak(text):
    """Function to speak out the given text."""
    engine.say(text)
    engine.runAndWait()

def wishMe():
    """Function to wish the user based on the time of the day."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Hello,  Good Morning")
    elif 12 <= hour < 18:
        speak("Hello,  Good Afternoon")
    else:
        speak("Hello,  Good Evening")

def takeCommand():
    """Function to take user's voice input and return the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        statement = recognizer.recognize_google(audio, language='en-in').lower()
        print(f"User said: {statement}\n")
    except Exception as e:
        speak("Pardon me, please say that again")
        return "None"
    
    return statement

def searchWikipedia(query):
    """Function to search Wikipedia for the given query."""
    speak('Searching Wikipedia...')
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=3)
    speak("According to Wikipedia")
    speak(results)

def openWebpage(url):
    """Function to open a webpage in the default web browser."""
    webbrowser.open_new_tab(url)
    speak(f"{url} is open now")
    time.sleep(5)

def getWeather(city_name):
    """Function to fetch and speak the weather information of a city."""
    api_key = "9f43880813ecb908bc961d341b20d279"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city_name}"
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        current_temperature = main["temp"]
        current_humidity = main["humidity"]
        weather_description = data["weather"][0]["description"]
        
        speak(f"Temperature: {current_temperature} Kelvin, Humidity: {current_humidity}%, Description: {weather_description}")
    else:
        speak("City Not Found")

def getTime():
    """Function to speak out the current time."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {current_time}")

# Add more functions for different functionalities like news, Stack Overflow, etc.

# Main function
if __name__ == '__main__':
    print('Loading your AI personal assistant - Sara')
    wishMe()

    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand()

        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('Your personal assistant Sara is shutting down, Goodbye')
            print('Your personal assistant Sara is shutting down, Goodbye')
            break

        if 'wikipedia' in statement:
            searchWikipedia(statement)

        elif 'open youtube' in statement:
            openWebpage("https://www.youtube.com")

        elif 'open google' in statement:
            openWebpage("https://www.google.com")

        elif 'open gmail' in statement:
            openWebpage("https://mail.google.com")

        elif "weather" in statement:
            speak("What's the city name?")
            city_name = takeCommand()
            getWeather(city_name)

        elif 'time' in statement:
            getTime()

        # Add more conditions for other functionalities

        elif 'close tab' in statement or 'close the tab' in statement:
            os.system("taskkill /im chrome.exe /f")
            speak("The tab has been closed.")

        # Add more conditions for other functionalities

    time.sleep(40)  # Sleep statement at the end (not sure why it's here)
