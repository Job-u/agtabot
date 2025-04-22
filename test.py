import re
import openai
import speech_recognition as sr
from playsound import playsound
from gtts import gTTS
import pygame
import os
import time
from unidecode import unidecode

class bot:
    exit_commands = ("bye", "exit", "ty", "thanks", "done", "quit", "stop")
    
    translations = {
        
    # Greetings and Common Phrases
    "What is your name?": {"filipino": "Ano ang pangalan mo?", "casiguran_agta": "anya i ngahen moa"},
    "Goodbye": {"filipino": "Paalam.", "casiguran_agta": "naydén kako dén"},
    "Thank you.": {"filipino": "Maraming salamat.", "casiguran_agta": "me ado a salamat"},
    "I am sorry.": {"filipino": "Patawarin mo ako.", "casiguran_agta": "Patawadén nék mo"},
    "Yes.": {"filipino": "Opo.", "casiguran_agta": "on"},
    "No.": {"filipino": "Hindi po.", "casiguran_agta": "ewan be"},
    "My name is .": {"filipino": "Ako si .", "casiguran_agta": "saken ti"},
    "Good to see you": {"filipino": "Buti na lang nakita kita", "casiguran_agta": "meta"},
    "How are you": {"filipino": "Kamusta ka na?", "casiguran_agta": "kumusta kam dén"},
    "I am fine": {"filipino": "Mabuti naman.", "casiguran_agta": "ma ige be"},
    "Glad to meet you": {"filipino": "Masaya akong makilala ka.", "casiguran_agta": "mesahat ék a matenggi taka"},
    "Good afternoon": {"filipino": "Magandang hapon", "casiguran_agta": "memahal a apon"},
    "Good evening": {"filipino": "Magandang gabi", "casiguran_agta": "memahal a kélép"},
    "Good morning": {"filipino": "Magandang umaga", "casiguran_agta": "memahal a gagabi"},
    "How about you": {"filipino": "Kayo po? / Ikaw?", "casiguran_agta": "sikam"},
    
    # Daily Use Expressions
    "Excuse me": {"filipino": "Makikiraan po.", "casiguran_agta": "mékidiman kame"},
    "I'm leaving": {"filipino": "Aalis na po ako.", "casiguran_agta": "még dema kamedén"},
    "Can you help me": {"filipino": "Maaari mo ba akong tulungan?", "casiguran_agta": "pwede ék moy tulungan"},
    "What can I do for you": {"filipino": "Ano po ang magagawa ko para sa inyo?", "casiguran_agta": "anya i magimet koa para dekam"},
    "I understand": {"filipino": "Naiintindihan ko.", "casiguran_agta": "meentendian ko"},
    
    # Question Words
    "What": {"filipino": "Ano?", "casiguran_agta": "anya"},
    "When": {"filipino": "Kailan?", "casiguran_agta": "ni kesya"},
    "Where": {"filipino": "Saan?", "casiguran_agta": "tahe"},
    "Which": {"filipino": "Alin?", "casiguran_agta": "nahe"},
    "Who": {"filipino": "Sino?", "casiguran_agta": "te esya"},
    "Why": {"filipino": "Bakit?", "casiguran_agta": "ata ay"},
    "How much": {"filipino": "Magkano?", "casiguran_agta": "sanganya?"},

    # Colors
    "Blue": {"filipino": "Asul", "casiguran_agta": "asul"},
    "Red": {"filipino": "Pula", "casiguran_agta": "medingat"},
    "White": {"filipino": "Puti", "casiguran_agta": "melatak"},
    "Black": {"filipino": "Itim", "casiguran_agta": "mengitet"},
    "Green": {"filipino": "Berde", "casiguran_agta": "kumanidon"},
    "Yellow": {"filipino": "Dilaw", "casiguran_agta": "medilaw"},
    "Brown": {"filipino": "Kulay tsokolate", "casiguran_agta": "tsokolate"},
    "Gray": {"filipino": "Kulay abo", "casiguran_agta": "kulay abo"},
    "Pink": {"filipino": "Rosas", "casiguran_agta": "rosas"},
    "Orange": {"filipino": "Dalandan", "casiguran_agta": "Kuman a don"},
    "Violet": {"filipino": "Lila", "casiguran_agta": "Kuman a pensél"},

    # Family Members
    "Grandfather": {"filipino": "Lolo", "casiguran_agta": "boboy lakay"},
    "Grandmother": {"filipino": "Lola", "casiguran_agta": "boboy bakés"},
    "Father": {"filipino": "Tatay", "casiguran_agta": "améng"},
    "Mother": {"filipino": "Nanay", "casiguran_agta": "inéng"},
    "Older Brother": {"filipino": "Kuya", "casiguran_agta": "kakéng"},
    "Older Sister": {"filipino": "Ate", "casiguran_agta": "kakéng"},
    "Youngest Sibling": {"filipino": "Bunso", "casiguran_agta": "depos"},
    "Husband": {"filipino": "Asawang lalaki", "casiguran_agta": "asawa a lalaki"},
    "Wife": {"filipino": "Asawang babae", "casiguran_agta": "asawa a babe"},
    "Son": {"filipino": "Anak na lalaki", "casiguran_agta": "anak a lalake"},
    "Daughter": {"filipino": "Anak na babae", "casiguran_agta": "anak a babe"},
    
    # Buying and Selling
    "How much for two": {"filipino": "Magkano ang dalawa?", "casiguran_agta": "sangan éduwa"},
    "I will get two": {"filipino": "Kukuha ako ng dalawa.", "casiguran_agta": "mangalap pékta éduwa"},
    "Okay, you can get them": {"filipino": "Sige kunin mo na.", "casiguran_agta": "nay alapén mo dén"},
    "It is fifty pesos": {"filipino": "Limampung piso ito.", "casiguran_agta": "lima apulo ye"},
    "The two are 100 pesos": {"filipino": "Isang daang piso ang dalawa.", "casiguran_agta": "esa a daan éduwa"},

    # Giving Directions
    "Where are you going": {"filipino": "Saan ka pupunta?", "casiguran_agta": "ahe ka umange"},
    "I'm going to the garden": {"filipino": "Pupunta ako sa halamanan.", "casiguran_agta": "ange ékta sikaw"},
    "Where is the garden": {"filipino": "Nasaan ang halamanan?", "casiguran_agta": "ahe to sikaw"},
    "The garden is by the river": {"filipino": "Malapit sa ilog ang halamanan.", "casiguran_agta": "adene ta dinom ya tu sikaw"},
    "Whose garden is it": {"filipino": "Kaninong halamanan iyon?", "casiguran_agta": "kini esya a sikaw ya"},
    "It is my garden": {"filipino": "Sa akin ang halamanan.", "casiguran_agta": "ko o ko a sikaw"}
    
    }

    audio_files = {
    "Family_Members": {
        "father": "audio_datasets/Family_Members/father.wav",
        "tatay": "audio_datasets/Family_Members/tatay.wav",
        "ameng": "audio_datasets/Family_Members/ameng.wav",
    },
    "Greetings": {
        "hello": "audio_datasets/Greetings/hello.wav",
        "good_morning": "audio_datasets/Greetings/good_morning.wav",
        "good_night": "audio_datasets/Greetings/good_night.wav",
    },
    "Colors": {
        "red": "audio_datasets/Colors/red.wav",
        "blue": "audio_datasets/Colors/blue.wav",
        "green": "audio_datasets/Colors/green.wav",
    },
    }

    def __init__(self):
        print("Greetings! Would you prefer to speak using a microphone or enter text manually?")
        print("'M' to speak using Microphone or 'T' to type your message")
        self.mode = input("Mode (M/T): ").strip().upper()
        self.recognizer = sr.Recognizer()
        pygame.mixer.init()  # Initialize the pygame mixer for audio playback

    def translate(self, userinput):
        # Clean the user input by removing special characters and accents
        userinput_clean = unidecode(userinput.lower())  # Remove accents and convert to lowercase

        # Loop through the translations and match
        for english, translations in self.translations.items():
            # Clean all variations to lowercase and remove accents for comparison
            english_clean = unidecode(english.lower())  # Remove accents and convert to lowercase
            filipino_clean = unidecode(translations['filipino'].lower())  # Same for Filipino translation
            agta_clean = unidecode(translations['casiguran_agta'].lower())  # Same for Agta translation

            # Adjust to allow partial matches or exact matches
            if userinput_clean == english_clean or userinput_clean == filipino_clean or userinput_clean == agta_clean:
                translation_text = f"English: {english}\nFilipino: {translations['filipino']}\nCasiguran Agta: {translations['casiguran_agta']}"
                return translation_text, english  # return the matched English keyword

        return "Oops! We don’t have a translation for that yet. Do you want to email us so we can add it?", None



    def voice_input(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            return ""
        except sr.RequestError:
            print("Speech service is not available right now.")
            return ""

    def play_pronunciation(self, text):
        """Generate and play pronunciation using gTTS if the audio file is not found."""
        try:
            # Generate pronunciation with gTTS
            tts = gTTS(text=text, lang='el')  # 'en' for English, change if needed
            temp_audio_path = "temp_pronunciation.mp3"  # Temporary file to store the audio
            tts.save(temp_audio_path)

            print("     🔊 Playing pronunciation...")
            # Play the generated audio
            pygame.mixer.music.load(temp_audio_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Clean up the temporary file after playing
            os.remove(temp_audio_path)
        except Exception as e:
            print(f"Error generating or playing audio: {e}")

    def chat(self):
        while True:
            if self.mode == 'T':
                userinput = input("Enter a word or phrase or type 'quit' to exit: ")
            else:
                userinput = self.voice_input()

            if userinput.lower() in self.exit_commands:
                print("Bot: Goodbye!")
                break

            print(f"\nYou: {userinput}")
            response, key = self.translate(userinput)
            print("Bot:", response)

            # If we found a valid key, attempt to play its pronunciation
            if key:
                audio_folder = "audio_dataset/Family_Members"  # Change depending on the category if needed
                filename = key.replace(" ", "_") + ".wav"  # Adjust to .wav for pronunciation audio
                audio_path = os.path.join(audio_folder, filename)

                if os.path.exists(audio_path):
                    print("     🔊 Playing pronunciation...")
                    pygame.mixer.music.load(audio_path)  # Load the .wav file
                    pygame.mixer.music.play()  # Play the audio
                    while pygame.mixer.music.get_busy():  # Wait until the sound is finished
                        pygame.time.Clock().tick(10)
                else:
                    print("     ❌ No pronunciation audio found, generating pronunciation...")
                    # Use TTS to play pronunciation dynamically if no file is found
                    self.play_pronunciation(response)
            print()  # extra space

# Create the bot instance and start the chat
AgtaBot = bot()
AgtaBot.chat()
