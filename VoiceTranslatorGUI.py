import tkinter as tk
from tkinter import StringVar, OptionMenu, Label, Button, Entry
from PIL import Image, ImageTk
from playsound3 import playsound
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import threading
import os


# Function to handle voice translation
def run_voice_translator():
    status_label.config(text="Listening...")
    app.update()

    def voice_translation_thread():
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening for speech...")
                voice = recognizer.listen(source, timeout=5)
                print("Processing speech...")

                source_lang = get_language_code(source_lang_menu.get())
                target_lang = get_language_code(target_lang_menu.get())

                # Recognize speech
                text = recognizer.recognize_google(voice, language=source_lang)
                print(f"Recognized text: {text}")
                status_label.config(text=f"Recognized: {text}")
                app.update()

                # Translate text
                translated_text = translate_text(text, target_lang)
                print(f"Translated text: {translated_text}")
                status_label.config(text=f"Translated: {translated_text}")
                app.update()

                # Play the translated text
                play_audio(translated_text, target_lang)
                print("Playing translation...")
                status_label.config(text="Translation played successfully!")
                save_translation(text, translated_text)
        except sr.UnknownValueError:
            print("Could not understand audio.")
            status_label.config(text="Error: Unable to recognize speech. Please try again.")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            status_label.config(text="Error: Microphone not detected or unavailable.")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            status_label.config(text=f"Unexpected error: {str(e)}")
        finally:
            print("Voice translation thread completed.")

    threading.Thread(target=voice_translation_thread, daemon=True).start()


# Function to handle manual text translation
def run_manual_translation():
    try:
        source_lang = get_language_code(source_lang_menu.get())
        target_lang = get_language_code(target_lang_menu.get())
        text = text_input.get()

        translated_text = translate_text(text, target_lang)
        print(f"Manual translation: {translated_text}")
        status_label.config(text=f"Translated: {translated_text}")
        play_audio(translated_text, target_lang)
        save_translation(text, translated_text)
    except Exception as e:
        print(f"Manual translation error: {str(e)}")
        status_label.config(text=f"Error: {str(e)}")


# Function to translate text
def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text


# Function to convert text to speech and play
def play_audio(text, language):
    audio_file = "output.mp3"
    tts = gTTS(text=text, lang=language)
    tts.save(audio_file)

    def play():
        try:
            playsound(audio_file)
        except Exception as e:
            print(f"Error playing audio: {e}")
            status_label.config(text="Error playing audio.")
        finally:
            if os.path.exists(audio_file):
                os.remove(audio_file)

    threading.Thread(target=play, daemon=True).start()


# Function to save translations to a file
def save_translation(original_text, translated_text):
    try:
        with open("translations.txt", "a", encoding="utf-8") as file:
            file.write(f"Original: {original_text}\nTranslated: {translated_text}\n\n")
        print("Translation saved.")
    except Exception as e:
        print(f"Error saving translation: {str(e)}")


# Function to retrieve language code from dropdown options
def get_language_code(full_name):
    for name, code in language_options:
        if name == full_name:
            return code


# Create the main app window
app = tk.Tk()
app.title("Voice Translator")
app.geometry("700x500")

# Load and set the background image
bg_image = Image.open("Language.jpg").resize((700, 500), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(app, width=700, height=500)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Add Title Label
title_label = Label(app, text="Voice Translator", font=("Arial", 20), bg="grey94")
canvas.create_window(350, 50, window=title_label)

# Language options
language_options = [
    ("English", "en"),
    ("Hindi", "hi"),
    ("Spanish", "es"),
    ("French", "fr"),
    ("German", "de"),
    ("Chinese (Simplified)", "zh-cn"),
    ("Arabic", "ar"),
    ("Russian", "ru"),
    ("Italian", "it"),
    ("Japanese", "ja"),
    ("Korean", "ko"),
    ("Portuguese", "pt"),
]

# Add Dropdown for Source Language
source_lang_label = Label(app, text="Source Language:", font=("Arial", 12), bg="grey94")
canvas.create_window(200, 120, window=source_lang_label)

source_lang_menu = StringVar(app)
source_lang_menu.set("English")
source_lang_dropdown = OptionMenu(app, source_lang_menu, *[lang[0] for lang in language_options])
canvas.create_window(200, 150, window=source_lang_dropdown)

# Add Dropdown for Target Language
target_lang_label = Label(app, text="Target Language:", font=("Arial", 12), bg="grey94")
canvas.create_window(500, 120, window=target_lang_label)

target_lang_menu = StringVar(app)
target_lang_menu.set("Hindi")
target_lang_dropdown = OptionMenu(app, target_lang_menu, *[lang[0] for lang in language_options])
canvas.create_window(500, 150, window=target_lang_dropdown)

# Add Manual Text Input
text_input_label = Label(app, text="Enter Text:", font=("Arial", 12), bg="grey94")
canvas.create_window(200, 200, window=text_input_label)

text_input = Entry(app, width=30, font=("Arial", 12))
canvas.create_window(400, 200, window=text_input)

# Add Status Label
status_label = Label(app, text="", font=("Arial", 12), wraplength=600, justify="center", bg="grey99")
canvas.create_window(350, 300, window=status_label)

# Add Buttons
start_button = Button(app, text="Start Voice Translation", font=("Arial", 14), command=run_voice_translator)
canvas.create_window(250, 400, window=start_button)

manual_button = Button(app, text="Translate Text", font=("Arial", 14), command=run_manual_translation)
canvas.create_window(450, 400, window=manual_button)

app.mainloop()
