import tkinter as tk
from tkinter import Button, Label
from gettext import translation
from playsound3 import playsound
from googletrans import Translator
import speech_recognition
from gtts import gTTS

def run_voice_translator():
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        label.config(text="Listening...")
        voice = recognizer.listen(source)
        text = recognizer.recognize_google(voice, language="fr")
        label.config(text=f"Recognized: {text}")

        translator = Translator()
        translation = translator.translate(text, dest="fr")
        label.config(text=f"Translated: {translation.text}")

        converted_audio = gTTS(translation.text, lang="fr")
        converted_audio.save("output.mp3")
        playsound("output.mp3")

app = tk.Tk()
app.title("Voice Translator")
app.geometry("400x200")

label = Label(app, text="Press the button and speak", wraplength=300)
label.pack(pady=20)

button = Button(app, text="Start Translation", command=run_voice_translator)
button.pack(pady=10)

app.mainloop()
